"""Optional JSON-RPC service for a running emulator stack."""

from __future__ import annotations

import asyncio
import itertools
import json
import logging
import socket
import threading
from collections.abc import Callable
from typing import Any, Self

from .stack import AsyncEmulatorStack

__all__ = ["AsyncEmulatorStackService", "EmulatorServiceClient"]

logger = logging.getLogger(__package__)


class _Error(Exception):
    def __init__(self, code: int, message: str) -> None:
        super().__init__(message)
        self.code = code


def _encode(value: Any) -> bytes:
    try:
        return (
            json.dumps(value, allow_nan=False, separators=(",", ":")).encode() + b"\n"
        )
    except (TypeError, ValueError) as exc:
        raise _Error(-32000, "value is not JSON compatible") from exc


class _Session:
    def __init__(
        self,
        service: AsyncEmulatorStackService,
        writer: asyncio.StreamWriter,
    ) -> None:
        self.service = service
        self.writer = writer
        self.subscriptions: set[str] = set()
        self.request_id: int | None = None
        self.done: asyncio.Future[None] | None = None
        self._call_lock = asyncio.Lock()

    async def send(self, message: dict[str, Any]) -> None:
        self.writer.write(_encode(message))
        await self.writer.drain()

    async def call(self, emulator: str, message: str) -> None:
        async with self._call_lock:
            if self.writer.is_closing():
                return
            self.request_id = next(self.service._request_ids)
            self.done = asyncio.get_running_loop().create_future()
            try:
                await self.send(
                    {
                        "jsonrpc": "2.0",
                        "id": self.request_id,
                        "method": "before_message",
                        "params": {"emulator": emulator, "message": message},
                    }
                )
                await asyncio.wait_for(self.done, self.service.session_timeout)
            except TimeoutError:
                logger.warning("emulator service session timed out")
                self.close()
            except (ConnectionError, OSError):
                self.close()
            finally:
                self.request_id = None
                self.done = None

    def complete(self, request: dict[str, Any]) -> None:
        if request.get("id") != self.request_id:
            return
        if "error" in request:
            logger.error("remote hook failed: %s", request["error"])
        if self.done is not None and not self.done.done():
            self.done.set_result(None)

    def close(self) -> None:
        self.writer.close()
        if self.done is not None and not self.done.done():
            self.done.set_result(None)


class _Connection:
    def __init__(self, service: AsyncEmulatorStackService, session: _Session) -> None:
        self.service = service
        self.session = session

    async def handle(self, reader: asyncio.StreamReader) -> None:
        while not self.session.writer.is_closing():
            request_id: Any = None
            try:
                line = await reader.readline()
                if not line:
                    return
                request = json.loads(line)
                if not isinstance(request, dict):
                    raise _Error(-32600, "invalid request")
                request_id = request.get("id")
                if "method" not in request:
                    self.session.complete(request)
                    continue
                params = request.get("params", {})
                if not isinstance(params, dict):
                    raise _Error(-32600, "invalid request")
                result = self.dispatch(request["method"], params)
                await self.reply(request_id, result=result)
            except _Error as exc:
                await self.reply(
                    request_id, error={"code": exc.code, "message": str(exc)}
                )
            except (json.JSONDecodeError, KeyError, TypeError):
                await self.reply(
                    request_id,
                    error={"code": -32600, "message": "invalid request"},
                )
            except (EOFError, OSError):
                return

    def dispatch(self, method: str, params: dict[str, Any]) -> Any:
        service = self.service
        if method == "subscribe":
            emulator = params.get("emulator")
            if emulator not in service.stack.emulators:
                raise _Error(-32602, "unknown emulator")
            self.session.subscriptions.add(emulator)
            return None

        if method not in {"get", "set"}:
            raise _Error(-32601, "method not found")
        if self.session.request_id is None:
            raise _Error(-32001, "context is available only inside a hook")

        emulator = params.get("emulator")
        key = params.get("key")
        if emulator not in service.stack.emulators or not isinstance(key, str):
            raise _Error(-32602, "invalid emulator or option key")
        options = service.stack.emulators[emulator].context.options

        if method == "get":
            if key not in options:
                raise _Error(-32602, "unknown context option")
            _encode(options[key])
            return options[key]

        if "value" not in params:
            raise _Error(-32602, "missing option value")
        _encode(params["value"])
        options[key] = params["value"]
        return None

    async def reply(
        self,
        request_id: Any,
        *,
        result: Any = None,
        error: dict[str, Any] | None = None,
    ) -> None:
        response = {"jsonrpc": "2.0", "id": request_id}
        response["error" if error else "result"] = error or result
        await self.session.send(response)


class AsyncEmulatorStackService:
    """Serve blocking stack hooks over JSON-RPC."""

    def __init__(
        self,
        stack: AsyncEmulatorStack,
        port: int,
        session_timeout: float,
    ) -> None:
        if not 1 <= port <= 65535:
            raise ValueError("port must be between 1 and 65535")
        if session_timeout <= 0:
            raise ValueError("session_timeout must be greater than zero")

        self.stack = stack
        self.port = port
        self.session_timeout = session_timeout
        self._sessions: set[_Session] = set()
        self._request_ids = itertools.count()
        self._server: asyncio.Server | None = None
        self._loop: asyncio.AbstractEventLoop | None = None
        self._thread: threading.Thread | None = None

        for name in stack.emulators:
            stack.before_message(name)(
                lambda message, name=name: self._before_message(name, message)
            )

    async def _handle(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        session = _Session(self, writer)
        self._sessions.add(session)
        try:
            await _Connection(self, session).handle(reader)
        finally:
            session.close()
            self._sessions.discard(session)
            await writer.wait_closed()

    def _before_message(self, emulator: str, message: str) -> None:
        if self._loop is not None:
            asyncio.run_coroutine_threadsafe(
                self._notify(emulator, message), self._loop
            ).result()

    async def _notify(self, emulator: str, message: str) -> None:
        for session in tuple(self._sessions):
            if emulator in session.subscriptions:
                await session.call(emulator, message)

    async def start(self) -> None:
        if self._server is not None:
            return
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(
            target=self._loop.run_forever, name="emulator-service", daemon=True
        )
        self._thread.start()
        try:
            self._server = await asyncio.wrap_future(
                asyncio.run_coroutine_threadsafe(
                    asyncio.start_server(self._handle, "localhost", self.port),
                    self._loop,
                )
            )
        except BaseException:
            await self._stop_loop()
            raise
        logger.info("emulator service listening on localhost:%s", self.port)

    async def shutdown(self) -> None:
        if self._server is None:
            return
        assert self._loop is not None
        await asyncio.wrap_future(
            asyncio.run_coroutine_threadsafe(self._shutdown_server(), self._loop)
        )
        self._server = None
        await self._stop_loop()

    async def _shutdown_server(self) -> None:
        assert self._server is not None
        self._server.close()
        for session in tuple(self._sessions):
            session.close()
        await self._server.wait_closed()
        while self._sessions:
            await asyncio.sleep(0)

    async def _stop_loop(self) -> None:
        assert self._loop is not None and self._thread is not None
        self._loop.call_soon_threadsafe(self._loop.stop)
        await asyncio.to_thread(self._thread.join)
        self._loop.close()
        self._loop = None
        self._thread = None

    async def __aenter__(self) -> Self:
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.shutdown()


class _Context:
    def __init__(self, client: EmulatorServiceClient, emulator: str) -> None:
        self.client = client
        self.emulator = emulator

    def get(self, key: str) -> Any:
        return self.client._context("get", self.emulator, key)

    def set(self, key: str, value: Any) -> None:
        self.client._context("set", self.emulator, key, value)


class EmulatorServiceClient:
    """Synchronous client for AsyncEmulatorStackService."""

    def __init__(self, host: str, port: int) -> None:
        self.socket = socket.create_connection((host, port))
        self.buffer = bytearray()
        self.ids = itertools.count()
        self.hooks: dict[str, list[Callable[[str], None]]] = {}
        self.in_hook = False

    def before_message(
        self, emulator: str
    ) -> Callable[[Callable[[str], None]], Callable[[str], None]]:
        def register(hook: Callable[[str], None]) -> Callable[[str], None]:
            if emulator not in self.hooks:
                self._request("subscribe", {"emulator": emulator})
                self.hooks[emulator] = []
            self.hooks[emulator].append(hook)
            return hook

        return register

    def __getitem__(self, emulator: str) -> _Context:
        return _Context(self, emulator)

    def _context(self, method: str, emulator: str, key: str, value: Any = None) -> Any:
        if not self.in_hook:
            raise RuntimeError("context is available only inside a hook")
        params = {"emulator": emulator, "key": key}
        if method == "set":
            params["value"] = value
        return self._request(method, params)

    def serve_forever(self) -> None:
        try:
            while True:
                self._handle(self._receive())
        except (EOFError, OSError):
            self.close()

    def _handle(self, request: dict[str, Any]) -> None:
        if request.get("method") != "before_message":
            return
        request_id = request.get("id")
        params = request.get("params", {})
        try:
            self.in_hook = True
            for hook in tuple(self.hooks.get(params["emulator"], ())):
                hook(params["message"])
            response = {"jsonrpc": "2.0", "id": request_id, "result": None}
        except Exception as exc:
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32000, "message": str(exc)},
            }
        finally:
            self.in_hook = False
        self._send(response)

    def _request(self, method: str, params: dict[str, Any]) -> Any:
        request_id = next(self.ids)
        self._send(
            {
                "jsonrpc": "2.0",
                "id": request_id,
                "method": method,
                "params": params,
            }
        )
        while True:
            response = self._receive()
            if response.get("id") == request_id and "method" not in response:
                if "error" in response:
                    raise RuntimeError(response["error"]["message"])
                return response.get("result")
            self._handle(response)

    def _send(self, message: dict[str, Any]) -> None:
        self.socket.sendall(_encode(message))

    def _receive(self) -> dict[str, Any]:
        while b"\n" not in self.buffer:
            data = self.socket.recv(65536)
            if not data:
                raise EOFError
            self.buffer.extend(data)
        line, _, rest = self.buffer.partition(b"\n")
        self.buffer = bytearray(rest)
        return json.loads(line)

    def close(self) -> None:
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        self.socket.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
