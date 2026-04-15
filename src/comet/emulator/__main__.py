"""Run instrument emulators as TCP sockets based on a simple `emulators.yaml`
configuration file.

Example configuration:

```
emulators:
  smu:
    model: urn:comet:model:keithley:2410
    port: 10001
  lcr:
    model: urn:comet:model:keysight:e4980a
    port: 11002
```

Loading a configuration filename (default filenames are `emulators.yaml` and `emulators.yml`).

```
python -m comet.emulator [-f emulators.yaml]
```

Hit Ctrl+C to stop all emulator sockets.

"""

import argparse
import asyncio
import contextlib
import logging
import os
import signal
from typing import Any

import schema
import yaml

from .. import __version__
from .emulator import emulator_factory
from .tcpserver import TCPServer, TCPServerContext

default_config_filenames: list[str] = ["emulators.yaml", "emulators.yml"]
default_host: str = "localhost"
default_termination: str = "\n"
default_request_delay: float = 0.1

termination_aliases: dict[str, str] = {
    "\r": "\r",
    "\n": "\n",
    "\r\n": "\r\n",
    "CR": "\r",
    "LF": "\n",
    "CRLF": "\r\n",
}


def normalize_termination(value: str) -> str:
    if value not in termination_aliases:
        raise schema.SchemaError(
            f"Invalid termination: {value!r}."
            f" Must be one of {list(termination_aliases)}"
        )
    return termination_aliases[value]


config_schema = schema.Schema(
    {
        schema.Optional("version"): str,
        "emulators": {
            str: {
                schema.Optional(schema.Or("model", "module")): str,
                schema.Optional("host"): str,
                "port": schema.And(
                    int,
                    lambda p: 1 <= p <= 65535,
                    error="port must be an integer between 1 and 65535",
                ),
                schema.Optional("termination"): schema.And(str, normalize_termination),
                schema.Optional("request_delay"): schema.And(
                    schema.Use(float), lambda d: d >= 0, error="request_delay must be >= 0"
                ),
                schema.Optional("options"): dict,
            }
        },
    }
)


def load_config(filename: str) -> dict[str, Any]:
    with open(filename) as fp:
        data = yaml.safe_load(fp)
    config = validate_config(data or {})
    for name, params in config.get("emulators", {}).items():
        if "model" in params and "module" in params:
            raise KeyError("keys 'model' and 'module' are exclusive")
        if "module" in params:
            logging.warning(
                "Emulator %r uses deprecated config key 'module'; "
                "use 'model' instead. Support exists only for backward compatibility.",
                name,
            )
        params.setdefault("host", default_host)
        params.setdefault("termination", default_termination)
        params.setdefault("request_delay", default_request_delay)
        params.setdefault("options", {})
    return config


def validate_config(config: dict[str, Any]) -> dict[str, Any]:
    return config_schema.validate(config)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        dest="filename",
        metavar="filename",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s version {__version__}",
        help="Print version information and quit",
    )
    return parser.parse_args()


def locate_config_filename() -> str:
    for filename in default_config_filenames:
        if os.path.isfile(filename):
            return filename
    raise RuntimeError("No config file found.")


async def async_main() -> None:
    args = parse_args()

    logging.basicConfig(level=logging.INFO)

    config = load_config(args.filename or locate_config_filename())

    servers: list[TCPServer] = []

    for name, params in config.get("emulators", {}).items():
        model = params.get("model") or params.get("module")  # fallback for comet<1.5
        host = params.get("host")
        port = params.get("port")
        termination_bytes = params.get("termination").encode()
        request_delay = params.get("request_delay")
        options = params.get("options", {})

        emulator = emulator_factory(model)()
        emulator.options.update(options)

        context = TCPServerContext(
            name=name,
            emulator=emulator,
            termination=termination_bytes,
            request_delay=request_delay,
            logger=logging.getLogger(name),
        )
        server = TCPServer((host, port), context)
        await server.start()
        servers.append(server)

    for server in servers:
        host, port = server.server_address
        server.context.logger.info("starting... %s:%s", host, port)

    stop_event = asyncio.Event()

    def request_shutdown() -> None:
        if not stop_event.is_set():
            for server in servers:
                host, port = server.server_address
                server.context.logger.info("stopping... %s:%s", host, port)
            stop_event.set()

    loop = asyncio.get_running_loop()

    for sig in (signal.SIGTERM, signal.SIGINT):
        try:
            loop.add_signal_handler(sig, request_shutdown)
        except NotImplementedError:
            # Not supported on some platforms (notably parts of Windows).
            # In that case, asyncio.run() will still surface Ctrl+C as
            # KeyboardInterrupt, handled outside main().
            ...

    tasks = [asyncio.create_task(server.serve_forever()) for server in servers]

    try:
        await stop_event.wait()
    finally:
        for server in servers:
            await server.shutdown()
        for task in tasks:
            task.cancel()
        for task in tasks:
            with contextlib.suppress(asyncio.CancelledError):
                await task


def main() -> None:
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        # Fallback for platforms where asyncio signal handlers are unavailable.
        ...


if __name__ == "__main__":
    main()
