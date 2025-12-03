"""Run instrument emulators as TCP sockets based on a simple `emulators.yaml`
configuration file.

Example configuration:

```
emulators:
  smu:
    module: keithley.k2410
    port: 10001
  lcr:
    module: keysight.e4980a
    port: 11002
  # User specific emulator
  my_instr:
    module: local_project.my_instr_emulator
    port: 12001
```

Loading a configuration filename (default filenames are `emulators.yaml` and `emulators.yml`).

```
python -m comet.emulator [-f emulators.yaml]
```

Hit Ctrl+C to stop all emulator sockets.

"""

import argparse
import logging
import os
import signal
import threading
from typing import Any

import schema
import yaml

from .. import __version__

from .emulator import emulator_factory
from .tcpserver import TCPServer, TCPServerThread, TCPServerContext

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
        schema.Optional("version"): str,  # deprecated
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
    # Set defaults
    for params in config.get("emulators", {}).values():
        if "model" in params and "module" in params:
            raise KeyError("keys 'model' and 'module' are exclusive")
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


def event_loop() -> None:
    """Blocks execution until termination or interrupt from keyboard signal."""
    e = threading.Event()

    def handle_event(signum, frame):
        e.set()

    signal.signal(signal.SIGTERM, handle_event)
    signal.signal(signal.SIGINT, handle_event)
    e.wait()


def main() -> None:
    args = parse_args()

    logging.basicConfig(level=logging.INFO)

    config = load_config(args.filename or locate_config_filename())

    threads = []

    for name, params in config.get("emulators", {}).items():
        model = params.get("model") or params.get("module") # fallback for comet<1.5
        host = params.get("host")
        port = params.get("port")
        termination_bytes = params.get("termination").encode()
        request_delay = params.get("request_delay")
        options = params.get("options", {})
        address = host, port
        emulator = emulator_factory(model)()
        emulator.options.update(options)
        context = TCPServerContext(
            name=name,
            emulator=emulator,
            termination=termination_bytes,
            request_delay=request_delay,
            logger=logging.getLogger(name),
        )
        server = TCPServer(address, context)
        threads.append(TCPServerThread(server))

    for thread in threads:
        host, port, *_ = thread.server.server_address  # IPv4/IPv6
        thread.server.context.logger.info("starting... %s:%s", host, port)
        thread.start()

    def handle_event(signum, frame):
        for thread in threads:
            host, port, *_ = thread.server.server_address  # IPv4/IPv6
            thread.server.context.logger.info("stopping... %s:%s", host, port)
            thread.shutdown()

    signal.signal(signal.SIGTERM, handle_event)
    signal.signal(signal.SIGINT, handle_event)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
