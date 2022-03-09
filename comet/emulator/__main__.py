import argparse
import logging
import os
import socketserver
import threading
import time

import schema
import yaml

from .emulator import emulator_factory

logger = logging.getLogger(__package__)


class TCPRequestHandler(socketserver.BaseRequestHandler):

    termination: str = '\r\n'

    delay: float = 0.1

    def read_messages(self):
        data = str(self.request.recv(4096), 'ascii')
        if not data:
            return None
        self.server.logger.info("recv %s", bytes(data, 'ascii'))
        return [line for line in data.split(self.termination) if line]

    def send_messages(self, response):
        if isinstance(response, (list, tuple)):
            response = self.termination.join(format(line) for line in response)
        data = bytes(f'{response}{self.termination}', 'ascii')
        self.server.logger.info("send %s", data)
        self.request.sendall(data)

    def apply_delay(self):
        time.sleep(self.delay)

    def handle(self):
        while True:
            messages = self.read_messages()
            if not messages:
                break
            if self.server.is_shutdown:
                break
            for message in messages:
                self.apply_delay()
                response = self.server.handler(message)
                if response is not None:
                    self.send_messages(response)


class TCPServer(socketserver.TCPServer):

    allow_reuse_address = True

    def __init__(self, address, handler):
        super().__init__(address, TCPRequestHandler)
        self.handler = handler
        self.shutdown_event = threading.Event()
        self.logger = logger.getChild(self.handler.name)

    @property
    def is_shutdown(self) -> bool:
        return self.shutdown_event.is_set()

    def shutdown(self):
        self.shutdown_event.set()
        super().shutdown()


class Thread(threading.Thread):

    def __init__(self, address, handler):
        super().__init__()
        self.server = TCPServer(address, handler)
        self.shutdown_request = threading.Event()

    def shutdown(self):
        self.shutdown_request.set()
        self.server.shutdown()

    def run(self):
        with self.server as server:
            server.serve_forever()


class Handler:

    def __init__(self, name, context):
        self.name = name
        self.context = context

    def __call__(self, data):
        return self.context(data)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', dest='filename', metavar='string', default=os.path.join('emulators.yaml'))
    return parser.parse_args()


version_schema = schema.Regex(r'^\d+\.\d+$')

config_schema = schema.Schema({
    'version': version_schema,
    'emulators': {
        str: {
            'type': str,
            schema.Optional('hostname'): str,
            'port': int
        }
    }
})


def load_config(filename):
    with open(filename) as fp:
        config = yaml.safe_load(fp)
    config_schema.validate(config)
    return config


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
        type_ = params.get('type')
        hostname = params.get('hostname', '')
        port = params.get('port')
        handler = Handler(name, emulator_factory(type_)())
        address = ('', port)
        threads.append(Thread(address, handler))

    for thread in threads:
        thread.server.logger.info("starting %s:%s", *thread.server.server_address)
        thread.start()

    event_loop()

    for thread in threads:
        thread.server.logger.info("stopping %s:%s", *thread.server.server_address)
        thread.shutdown()

    for thread in threads:
        thread.join()

    return 0


if __name__ == '__main__':
    main()
