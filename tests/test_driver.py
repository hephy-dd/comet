import struct
from typing import List

import pytest


def pack_bianry_values(values) -> bytes:
    payload = struct.pack("<" + "f" * len(values), *values)
    header = f"#{len(str(len(payload)))}{len(payload)}".encode("ascii")
    return header + payload


def unpack_binary_values(data: bytes) -> List[float]:
    if not data.startswith(b"#"):
        raise ValueError("Invalid block: must start with '#'")

    # Read header
    n_digits = int(chr(data[1]))  # how many digits in the length field
    length_str = data[2:2+n_digits].decode("ascii")
    payload_len = int(length_str)

    # Slice out the binary payload
    start = 2 + n_digits
    payload = data[start:start+payload_len]

    if len(payload) != payload_len:
        raise ValueError("Invalid block: payload length mismatch")

    # Each float32 is 4 bytes
    if payload_len % 4 != 0:
        raise ValueError("Invalid block: payload not multiple of 4 bytes")

    count = payload_len // 4
    floats = struct.unpack("<" + "f"*count, payload)
    return list(floats)



class MockResource:

    def __init__(self):
        self.buffer = []

    def clear(self):
        ...  # VISA bus clear

    def read(self):
        return self.buffer.pop(0)

    def write(self, message):
        self.buffer.append(message)

    def query(self, message):
        self.write(message)
        return self.read()

    def read_bytes(self, count: int) -> bytes:
        self.buffer.pop(0)

    def write_raw(self, message: bytes) -> int:
        self.buffer.append(message)

    def query_binary_values(self, message: str, *, datatype="f", is_big_endian=False):
        self.write(message)
        return unpack_binary_values(self.buffer.pop(0))


@pytest.fixture
def resource():
    return MockResource()
