import argparse
import asyncio
import contextlib
import inspect
import logging
import re
import signal
from dataclasses import dataclass
from typing import Iterable, Optional, Union

from .emulator import Emulator
from .response import Response

__all__ = ["TCPRequestHandler", "TCPServer", "TCPServerContext"]


class TCPRequestHandler:
    async def read_messages(
        self,
        reader: asyncio.StreamReader,
        context: "TCPServerContext",
        rx_buffer: bytearray,
    ) -> Optional[list[bytes]]:
        data = await reader.read(4096)
        if not data:
            return None

        context.logger.info("recv %s", data)
        rx_buffer.extend(data)

        termination_bytes = context.termination
        messages: list[bytes] = []

        while (pos := rx_buffer.find(termination_bytes)) >= 0:
            message = rx_buffer[:pos]
            del rx_buffer[: pos + len(termination_bytes)]
            messages.append(bytes(message))

        return messages

    async def send_messages(
        self,
        writer: asyncio.StreamWriter,
        context: "TCPServerContext",
        response: Union[Response, Iterable[Response]],
    ) -> None:
        termination_bytes = context.termination

        if isinstance(response, Response):
            responses = [response]
        else:
            responses = list(response)

        buffer = bytearray()
        for res in responses:
            buffer.extend(bytes(res))
            # TODO: most instruments append termination also to binary
            buffer.extend(termination_bytes)

        data = bytes(buffer)
        context.logger.info("send %s", data)
        writer.write(data)
        await writer.drain()

    async def handle(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        context: "TCPServerContext",
    ) -> None:
        rx_buffer = bytearray()

        try:
            while True:
                messages = await self.read_messages(reader, context, rx_buffer)
                if messages is None:
                    break

                for message in messages:
                    response = await context.handle_message(str(message, "utf-8"))
                    if response is not None:
                        await self.send_messages(writer, context, response)
        except asyncio.CancelledError:
            raise
        finally:
            writer.close()
            with contextlib.suppress(Exception):
                await writer.wait_closed()


@dataclass
class TCPServerContext:
    name: str
    emulator: Emulator
    termination: bytes
    request_delay: float
    logger: logging.Logger

    async def handle_message(
        self,
        message: str,
    ) -> Union[None, Response, Iterable[Response]]:
        response = self.emulator(message)
        if response is not None:
            await asyncio.sleep(self.request_delay)
        return response


class TCPServer:
    def __init__(self, address: tuple[str, int], context: TCPServerContext) -> None:
        self.address = address
        self.context = context
        self._server: Optional[asyncio.base_events.Server] = None
        self._handler = TCPRequestHandler()
        self._shutdown_lock = asyncio.Lock()
        self._shutdown_started = False

    @property
    def server_address(self) -> tuple[str, int]:
        if self._server is None or not self._server.sockets:
            return self.address

        sockname = self._server.sockets[0].getsockname()
        return sockname[:2]

    async def start(self) -> None:
        if self._server is not None:
            return

        self._server = await asyncio.start_server(
            lambda r, w: self._handler.handle(r, w, self.context),
            host=self.address[0],
            port=self.address[1],
            reuse_address=True,
        )

    async def serve_forever(self) -> None:
        if self._server is None:
            await self.start()

        assert self._server is not None
        async with self._server:
            await self._server.serve_forever()

    async def shutdown(self) -> None:
        async with self._shutdown_lock:
            if self._shutdown_started:
                return
            self._shutdown_started = True

            if self._server is not None:
                self._server.close()
                await self._server.wait_closed()


def option_type(value: str) -> tuple[str, str]:
    m = re.match(r"^([A-Za-z0-9][A-Za-z0-9_.:+/-]*)=(.*)$", value)
    if m:
        return m.group(1), m.group(2)

    raise argparse.ArgumentTypeError("expected 'key=value'")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost", help="host, default is 'localhost'")
    parser.add_argument("-p", "--port", type=int, default=10000, help="port, default is 10000")
    parser.add_argument(
        "-t",
        "--termination",
        default="\n",
        choices=["\r", "\n", "\r\n"],
        help="message termination, default is '\\n'",
    )
    parser.add_argument(
        "-d",
        "--request-delay",
        type=float,
        default=0.1,
        help="delay between requests in seconds, default is 0.1 sec",
    )
    parser.add_argument(
        "-o",
        "--option",
        type=option_type,
        action="append",
        default=[],
        help="set emulator specific option(s), e.g. '-o version=2.1'",
    )
    return parser.parse_args()


def run(emulator: Emulator) -> int:
    """Convenience emulator runner using asyncio TCP server."""
    if not isinstance(emulator, Emulator):
        raise TypeError(f"Emulator must inherit from {Emulator}")

    args = parse_args()
    emulator.options.update({key: value for key, value in args.option})

    logging.basicConfig(level=logging.INFO)

    mod = inspect.getmodule(emulator.__class__)
    name = (
        getattr(getattr(mod, "__spec__", None), "name", None)
        or emulator.__class__.__module__
    )

    context = TCPServerContext(
        name=name,
        emulator=emulator,
        termination=args.termination.encode(),
        request_delay=args.request_delay,
        logger=logging.getLogger(name),
    )
    address = (args.host, args.port)

    async def main() -> None:
        server = TCPServer(address, context)
        await server.start()

        host, port = server.server_address
        context.logger.info("starting... %s:%s", host, port)

        stop_event = asyncio.Event()

        def request_shutdown() -> None:
            if stop_event.is_set():
                return

            context.logger.info("stopping... %s:%s", host, port)
            stop_event.set()

        loop = asyncio.get_running_loop()
        installed_signals: list[int] = []

        for sig in (signal.SIGTERM, signal.SIGINT):
            try:
                loop.add_signal_handler(sig, request_shutdown)
                installed_signals.append(sig)
            except NotImplementedError:
                # Not supported on some platforms (notably parts of Windows).
                # In that case, asyncio.run() will still surface Ctrl+C as
                # KeyboardInterrupt, handled outside main().
                ...

        serve_task = asyncio.create_task(server.serve_forever())

        try:
            await stop_event.wait()
        finally:
            await server.shutdown()

            serve_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await serve_task

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Fallback for platforms where asyncio signal handlers are unavailable.
        ...

    return 0
