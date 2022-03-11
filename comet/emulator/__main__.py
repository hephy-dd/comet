"""Run instrument emulators as TCP sockets based on a simple `emulators.yaml`
configuration file.

Example configuration:

```
version: '1.0'
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

Executing a configuration filename (default filename is `emulators.yaml`).

```
python -m comet.emulator [-f emulators.yaml]
```

Hit Ctrl+C to stop all emulator sockets.

"""

import argparse
import logging
import socketserver
import threading
import time

import schema
import yaml

from .emulator import emulator_factory
from .tcpserver import TCPServer, TCPServerThread, TCPServerContext

default_config_filename = 'emulators.yaml'
default_hostname: str  = ''
default_termination: str = '\r\n'
default_request_delay: float = 0.1

version_schema = schema.Regex(r'^\d+\.\d+$')

config_schema = schema.Schema({
    'version': version_schema,
    'emulators': {
        str: {
            'module': str,
            schema.Optional('hostname'): str,
            'port': int,
            schema.Optional('termination'): str,
            schema.Optional('request_delay'): float,
        }
    }
})


def load_config(filename: str) -> dict:
    with open(filename) as fp:
        config = yaml.safe_load(fp)
    # Set defaults
    for params in config.get('emulators', {}).values():
        params.setdefault('hostname', default_hostname)
        params.setdefault('termination', default_termination)
        params.setdefault('request_delay', default_request_delay)
    # Validate config
    validate_config(config)
    return config


def validate_config(config: dict) -> None:
    config_schema.validate(config)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', dest='filename', metavar='string', default=default_config_filename)
    return parser.parse_args()


def event_loop() -> None:
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        ...


def main() -> int:
    args = parse_args()

    logging.basicConfig(level=logging.INFO)

    config = load_config(args.filename)

    threads = []

    for name, params in config.get('emulators', {}).items():
        module = params.get('module')
        hostname = params.get('hostname')
        port = params.get('port')
        termination = params.get('termination')
        request_delay = params.get('request_delay')
        address = hostname, port
        emulator = emulator_factory(module)()
        context = TCPServerContext(name, emulator, termination, request_delay)
        server = TCPServer(address, context)
        threads.append(TCPServerThread(server))

    for thread in threads:
        hostname, port = thread.server.server_address
        thread.server.context.logger.info("starting... %s:%s", hostname, port)
        thread.start()

    event_loop()

    for thread in threads:
        hostname, port = thread.server.server_address
        thread.server.context.logger.info("stopping... %s:%s", hostname, port)
        thread.shutdown()

    for thread in threads:
        thread.join()

    return 0


if __name__ == '__main__':
    main()
