import asyncio
import logging
import os
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Final, Self, TextIO

import schema
import yaml

from .emulator import Context, Emulator, emulator_cls_factory
from .tcpserver import TCPServer, TCPServerContext

__all__ = ["AsyncEmulatorStack", "EmulatorStack"]

DEFAULT_CONFIG_FILES: Final[list[str]] = [
    "emulators.yaml",
    "emulators.yml",
    "emulators.json",
]

TERMINATION_ALIASES: Final[dict[str, str]] = {
    "\r": "\r",
    "\n": "\n",
    "\r\n": "\r\n",
    "CR": "\r",
    "LF": "\n",
    "CRLF": "\r\n",
    "": "",
}

logger = logging.getLogger(__package__)


@dataclass(slots=True, frozen=True)
class EmulatorConfig:
    model: str
    port: int
    host: str = "localhost"
    termination: str = "\n"
    request_delay: float = 0.1
    options: dict[str, Any] = field(default_factory=dict)


def normalize_termination(value: str) -> str:
    if value not in TERMINATION_ALIASES:
        raise schema.SchemaError(
            f"Invalid termination: {value!r}."
            f" Must be one of {list(TERMINATION_ALIASES)}"
        )
    return TERMINATION_ALIASES[value]


config_schema = schema.Schema(
    {
        schema.Optional("version"): str,
        "emulators": {
            str: {
                schema.Optional(schema.Or("model", "module")): str,  # type: ignore
                schema.Optional("host"): str,
                "port": schema.And(
                    int,
                    lambda p: 1 <= p <= 65535,
                    error="port must be an integer between 1 and 65535",
                ),
                schema.Optional("termination"): schema.And(
                    str,
                    schema.Use(normalize_termination),  # type: ignore
                ),
                schema.Optional("request_delay"): schema.And(
                    schema.Use(float),  # type: ignore
                    lambda d: d >= 0,
                    error="request_delay must be >= 0",
                ),
                schema.Optional("options"): dict,
            }
        },
    }
)


def load_config(filename: str) -> dict[str, Any]:
    with open(filename) as fp:
        data = yaml.safe_load(fp)
    return normalize_config(data or {})


def locate_config_filename() -> str:
    filenames = [
        filename for filename in DEFAULT_CONFIG_FILES if os.path.isfile(filename)
    ]

    if not filenames:
        supported = ", ".join(repr(filename) for filename in DEFAULT_CONFIG_FILES)
        raise FileNotFoundError(
            f"No default config file found; expected one of: {supported}"
        )

    filename = filenames[0]

    if len(filenames) > 1:
        logger.warning(
            "Found multiple default config files: %s",
            ", ".join(filenames),
        )
        logger.warning("Using %s", filename)

    return filename


def normalize_config(
    config: Mapping[str, Any],
) -> dict[str, EmulatorConfig]:
    config = config_schema.validate(dict(config))

    emulators = {}

    for name, params in config.get("emulators", {}).items():
        if "model" in params and "module" in params:
            raise KeyError("keys 'model' and 'module' are exclusive")

        if "module" in params:
            logger.warning(
                "Emulator %r uses deprecated config key 'module'; "
                "use 'model' instead. Support exists only for backward compatibility.",
                name,
            )
            params["model"] = params.pop("module")

        emulators[name] = EmulatorConfig(**params)

    return emulators


BeforeMessageHook = Callable[[str], None]


class AsyncEmulatorStack:
    def __init__(self, config: Mapping[str, EmulatorConfig]) -> None:
        self.config: dict[str, EmulatorConfig] = dict(config)
        self.emulators: dict[str, Emulator] = {}
        self.servers: dict[str, TCPServer] = {}
        self._before_message_hooks: dict[str, list[BeforeMessageHook]] = {}
        self._build()

    @classmethod
    def from_config(cls, config: Mapping[str, Any]) -> Self:
        return cls(normalize_config(config))

    @classmethod
    def from_file(cls, config_file: str | Path | TextIO | None = None) -> Self:
        if config_file is None:
            config_file = locate_config_filename()

        if isinstance(config_file, (str, Path)):
            with open(config_file) as fp:
                config = yaml.safe_load(fp)
        else:
            config = yaml.safe_load(config_file)

        return cls.from_config(config or {})

    async def start(self) -> None:
        for server in self.servers.values():
            await server.start()

            host, port = server.server_address
            server.context.logger.info("starting... %s:%s", host, port)

    async def serve_forever(self) -> None:
        await asyncio.gather(
            *(server.serve_forever() for server in self.servers.values())
        )

    async def shutdown(self) -> None:
        for server in self.servers.values():
            host, port = server.server_address
            server.context.logger.info("stopping... %s:%s", host, port)

        await asyncio.gather(*(server.shutdown() for server in self.servers.values()))

    def _build(self) -> None:
        for name, config in self.config.items():
            context = Context(options=config.options)
            cls = emulator_cls_factory(config.model)
            emulator = cls(context)

            server_context = TCPServerContext(
                name=name,
                emulator=emulator,
                termination=config.termination.encode(),
                request_delay=config.request_delay,
                logger=logging.getLogger(name),
                before_message=self._before_message,
            )

            server = TCPServer((config.host, config.port), server_context)

            self.emulators[name] = emulator
            self.servers[name] = server

    def before_message(
        self, name: str
    ) -> Callable[[BeforeMessageHook], BeforeMessageHook]:
        def register(hook: BeforeMessageHook) -> BeforeMessageHook:
            self._before_message_hooks.setdefault(name, []).append(hook)
            return hook

        return register

    def _before_message(self, name: str, message: str) -> None:
        for hook in self._before_message_hooks.get(name, ()):
            hook(message)

    def __getitem__(self, name: str) -> Emulator:
        return self.emulators[name]

    async def __aenter__(self) -> Self:
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.shutdown()


class EmulatorStack:
    def __init__(self, stack: AsyncEmulatorStack) -> None:
        self._stack = stack

    @classmethod
    def from_config(cls, config: Mapping[str, Any]) -> Self:
        return cls(AsyncEmulatorStack.from_config(config))

    @classmethod
    def from_file(
        cls,
        config_file: str | Path | TextIO | None = None,
    ) -> Self:
        return cls(AsyncEmulatorStack.from_file(config_file))

    def serve_forever(self) -> None:
        asyncio.run(self._serve_forever())

    async def _serve_forever(self) -> None:
        async with self._stack:
            await self._stack.serve_forever()

    def before_message(
        self, name: str
    ) -> Callable[[BeforeMessageHook], BeforeMessageHook]:
        return self._stack.before_message(name)

    def __getitem__(self, name: str) -> Emulator:
        return self._stack.emulators[name]
