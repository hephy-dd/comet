import argparse
import logging
import types

import pytest

from comet.emulator import tcpserver


class FakeResponse:
    def __init__(self, payload: bytes):
        self.payload = payload

    def __bytes__(self) -> bytes:
        return self.payload


class FakeStreamReader:
    def __init__(self, chunks):
        self._chunks = list(chunks)

    async def read(self, n: int) -> bytes:
        if self._chunks:
            return self._chunks.pop(0)
        return b""


class FakeStreamWriter:
    def __init__(self):
        self.writes = []
        self.drained = 0
        self.closed = False
        self.wait_closed_called = False

    def write(self, data: bytes) -> None:
        self.writes.append(data)

    async def drain(self) -> None:
        self.drained += 1

    def close(self) -> None:
        self.closed = True

    async def wait_closed(self) -> None:
        self.wait_closed_called = True


class DummyLogger:
    def __init__(self):
        self.records = []

    def info(self, msg, *args):
        if args:
            msg = msg % args
        self.records.append(msg)


class DummyContext:
    def __init__(self, termination=b"\n", handle_result=None):
        self.termination = termination
        self.logger = DummyLogger()
        self._handle_result = handle_result
        self.messages = []

    async def handle_message(self, message: str):
        self.messages.append(message)
        return self._handle_result


@pytest.fixture
def patch_response(monkeypatch):
    monkeypatch.setattr(tcpserver, "Response", FakeResponse)
    return FakeResponse


@pytest.mark.asyncio
async def test_read_messages_returns_none_on_eof():
    handler = tcpserver.TCPRequestHandler()
    reader = FakeStreamReader([b""])
    context = DummyContext()
    rx_buffer = bytearray()

    result = await handler.read_messages(reader, context, rx_buffer)

    assert result is None
    assert rx_buffer == bytearray()
    assert context.logger.records == []


@pytest.mark.asyncio
async def test_read_messages_splits_complete_messages():
    handler = tcpserver.TCPRequestHandler()
    reader = FakeStreamReader([b"CMD1\nCMD2\n"])
    context = DummyContext(termination=b"\n")
    rx_buffer = bytearray()

    result = await handler.read_messages(reader, context, rx_buffer)

    assert result == [b"CMD1", b"CMD2"]
    assert rx_buffer == bytearray()
    assert context.logger.records == ["recv b'CMD1\\nCMD2\\n'"]


@pytest.mark.asyncio
async def test_read_messages_preserves_partial_frame():
    handler = tcpserver.TCPRequestHandler()
    context = DummyContext(termination=b"\r\n")
    rx_buffer = bytearray()

    result1 = await handler.read_messages(
        FakeStreamReader([b"ONE\r\nTWO\r"]),
        context,
        rx_buffer,
    )
    assert result1 == [b"ONE"]
    assert rx_buffer == bytearray(b"TWO\r")

    result2 = await handler.read_messages(
        FakeStreamReader([b"\nTHREE\r\n"]),
        context,
        rx_buffer,
    )
    assert result2 == [b"TWO", b"THREE"]
    assert rx_buffer == bytearray()


@pytest.mark.asyncio
async def test_send_messages_single_response(patch_response):
    handler = tcpserver.TCPRequestHandler()
    writer = FakeStreamWriter()
    context = DummyContext(termination=b"\n")

    await handler.send_messages(writer, context, FakeResponse(b"OK"))

    assert writer.writes == [b"OK\n"]
    assert writer.drained == 1
    assert context.logger.records == ["send b'OK\\n'"]


@pytest.mark.asyncio
async def test_send_messages_multiple_responses(patch_response):
    handler = tcpserver.TCPRequestHandler()
    writer = FakeStreamWriter()
    context = DummyContext(termination=b"\r\n")

    responses = [FakeResponse(b"A"), FakeResponse(b"B")]
    await handler.send_messages(writer, context, responses)

    assert writer.writes == [b"A\r\nB\r\n"]
    assert writer.drained == 1
    assert context.logger.records == ["send b'A\\r\\nB\\r\\n'"]


@pytest.mark.asyncio
async def test_handle_reads_dispatches_sends_and_closes_writer(monkeypatch, patch_response):
    handler = tcpserver.TCPRequestHandler()
    context = DummyContext(handle_result=FakeResponse(b"RSP"))
    writer = FakeStreamWriter()

    async def fake_read_messages(reader, context, rx_buffer):
        if not hasattr(fake_read_messages, "count"):
            fake_read_messages.count = 0
        fake_read_messages.count += 1
        if fake_read_messages.count == 1:
            return [b"PING", b"PONG"]
        return None

    sent = []

    async def fake_send_messages(writer, context, response):
        sent.append(bytes(response))

    monkeypatch.setattr(handler, "read_messages", fake_read_messages)
    monkeypatch.setattr(handler, "send_messages", fake_send_messages)

    await handler.handle(object(), writer, context)

    assert context.messages == ["PING", "PONG"]
    assert sent == [b"RSP", b"RSP"]
    assert writer.closed is True
    assert writer.wait_closed_called is True


@pytest.mark.asyncio
async def test_handle_closes_writer_even_if_handle_message_raises():
    handler = tcpserver.TCPRequestHandler()
    writer = FakeStreamWriter()

    class ExplodingContext(DummyContext):
        async def handle_message(self, message: str):
            raise RuntimeError("boom")

    context = ExplodingContext()

    async def fake_read_messages(reader, context, rx_buffer):
        return [b"PING"]

    handler.read_messages = fake_read_messages

    with pytest.raises(RuntimeError, match="boom"):
        await handler.handle(object(), writer, context)

    assert writer.closed is True
    assert writer.wait_closed_called is True


@pytest.mark.asyncio
async def test_context_handle_message_waits_only_when_response(monkeypatch):
    sleep_calls = []

    async def fake_sleep(delay):
        sleep_calls.append(delay)

    monkeypatch.setattr(tcpserver.asyncio, "sleep", fake_sleep)

    class DummyEmulator:
        def __init__(self, response):
            self.response = response

        def __call__(self, message):
            return self.response

    ctx1 = tcpserver.TCPServerContext(
        name="x",
        emulator=DummyEmulator("ok"),
        termination=b"\n",
        request_delay=0.25,
        logger=logging.getLogger("test1"),
    )
    ctx2 = tcpserver.TCPServerContext(
        name="x",
        emulator=DummyEmulator(None),
        termination=b"\n",
        request_delay=0.25,
        logger=logging.getLogger("test2"),
    )

    assert await ctx1.handle_message("cmd") == "ok"
    assert sleep_calls == [0.25]

    assert await ctx2.handle_message("cmd") is None
    assert sleep_calls == [0.25]


def test_server_address_returns_configured_address_before_start():
    ctx = DummyContext()
    server = tcpserver.TCPServer(("127.0.0.1", 5555), ctx)

    assert server.server_address == ("127.0.0.1", 5555)


def test_server_address_returns_bound_socket_address_after_start():
    ctx = DummyContext()
    server = tcpserver.TCPServer(("127.0.0.1", 5555), ctx)

    class DummySocket:
        def getsockname(self):
            return ("127.0.0.1", 6000, "ignored")

    server._server = types.SimpleNamespace(sockets=[DummySocket()])

    assert server.server_address == ("127.0.0.1", 6000)


@pytest.mark.asyncio
async def test_server_start_uses_asyncio_start_server(monkeypatch):
    ctx = DummyContext()
    server = tcpserver.TCPServer(("localhost", 1234), ctx)

    created = {}

    class DummyAsyncServer:
        sockets = []

    async def fake_start_server(callback, host, port, reuse_address):
        created["callback"] = callback
        created["host"] = host
        created["port"] = port
        created["reuse_address"] = reuse_address
        return DummyAsyncServer()

    monkeypatch.setattr(tcpserver.asyncio, "start_server", fake_start_server)

    await server.start()

    assert isinstance(server._server, DummyAsyncServer)
    assert created["host"] == "localhost"
    assert created["port"] == 1234
    assert created["reuse_address"] is True
    assert callable(created["callback"])


@pytest.mark.asyncio
async def test_server_shutdown_closes_server():
    ctx = DummyContext()
    server = tcpserver.TCPServer(("localhost", 1234), ctx)

    class DummyAsyncServer:
        def __init__(self):
            self.closed = False
            self.wait_closed_called = False

        def close(self):
            self.closed = True

        async def wait_closed(self):
            self.wait_closed_called = True

    dummy = DummyAsyncServer()
    server._server = dummy

    await server.shutdown()

    assert dummy.closed is True
    assert dummy.wait_closed_called is True


def test_option_type_parses_valid_key_value():
    assert tcpserver.option_type("version=2.1") == ("version", "2.1")
    assert tcpserver.option_type("a_b.c:+/-=value") == ("a_b.c:+/-", "value")


def test_option_type_rejects_invalid_key():
    with pytest.raises(argparse.ArgumentTypeError, match="expected 'key=value'"):
        tcpserver.option_type("=value")


def test_parse_args_defaults(monkeypatch):
    monkeypatch.setattr(tcpserver.argparse.ArgumentParser, "parse_args", lambda self: argparse.Namespace(
        host="localhost",
        port=10000,
        termination="\n",
        request_delay=0.1,
        option=[],
    ))

    args = tcpserver.parse_args()

    assert args.host == "localhost"
    assert args.port == 10000
    assert args.termination == "\n"
    assert args.request_delay == 0.1
    assert args.option == []


def test_run_rejects_non_emulator():
    with pytest.raises(TypeError, match="Emulator must inherit from"):
        tcpserver.run(object())


def test_run_configures_options_and_returns_zero(monkeypatch):
    class BaseEmulator:
        def __init__(self):
            self.options = {}

    monkeypatch.setattr(tcpserver, "Emulator", BaseEmulator)

    emulator = BaseEmulator()

    monkeypatch.setattr(
        tcpserver,
        "parse_args",
        lambda: argparse.Namespace(
            host="127.0.0.1",
            port=9999,
            termination="\n",
            request_delay=0.01,
            option=[("mode", "test"), ("version", "1")],
        ),
    )

    monkeypatch.setattr(tcpserver.inspect, "getmodule", lambda cls: types.SimpleNamespace(__spec__=types.SimpleNamespace(name="pkg.tcpserver")))

    ran = {}

    def fake_asyncio_run(coro):
        ran["called"] = True
        coro.close()

    monkeypatch.setattr(tcpserver.asyncio, "run", fake_asyncio_run)

    rc = tcpserver.run(emulator)

    assert rc == 0
    assert ran["called"] is True
    assert emulator.options == {"mode": "test", "version": "1"}
