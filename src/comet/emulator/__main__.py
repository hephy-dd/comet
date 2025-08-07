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

import schema
import yaml

from .emulator import emulator_factory
from .tcpserver import TCPServer, TCPServerThread, TCPServerContext

default_config_filenames: list[str] = ["emulators.yaml", "emulators.yml"]
default_hostname: str = ""
default_termination: str = "\r\n"
default_request_delay: float = 0.1

config_schema = schema.Schema(
    {
        schema.Optional("version"): str,  # deprecated
        "emulators": {
            str: {
                "module": str,
                schema.Optional("hostname"): str,
                "port": int,
                schema.Optional("termination"): str,
                schema.Optional("request_delay"): float,
                schema.Optional("options"): dict,
            }
        },
    }
)


def load_config(filename: str) -> dict:
    with open(filename) as fp:
        data = yaml.safe_load(fp)
    config = validate_config(data or {})
    # Set defaults
    for params in config.get("emulators", {}).values():
        params.setdefault("hostname", default_hostname)
        params.setdefault("termination", default_termination)
        params.setdefault("request_delay", default_request_delay)
        params.setdefault("options", {})
    return config


def validate_config(config: dict) -> dict:
    return config_schema.validate(config)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        dest="filename",
        metavar="filename",
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
        module = params.get("module")
        hostname = params.get("hostname")
        port = params.get("port")
        termination = params.get("termination")
        request_delay = params.get("request_delay")
        options = params.get("options", {})
        address = hostname, port
        emulator = emulator_factory(module)()
        emulator.options.update(options)
        context = TCPServerContext(name, emulator, termination, request_delay)
        server = TCPServer(address, context)
        threads.append(TCPServerThread(server))

    for thread in threads:
        hostname, port, *_ = thread.server.server_address  # IPv4/IPv6
        thread.server.context.logger.info("starting... %s:%s", hostname, port)
        thread.start()

    def handle_event(signum, frame):
        for thread in threads:
            hostname, port, *_ = thread.server.server_address  # IPv4/IPv6
            thread.server.context.logger.info("stopping... %s:%s", hostname, port)
            thread.shutdown()

    signal.signal(signal.SIGTERM, handle_event)
    signal.signal(signal.SIGINT, handle_event)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
