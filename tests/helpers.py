import struct

__all__ = [
    "pack_binary_values",
    "unpack_binary_values",
    "MockResource",
]


def pack_binary_values(values) -> bytes:
    payload = struct.pack("<" + "f" * len(values), *values)
    header = f"#{len(str(len(payload)))}{len(payload)}".encode("ascii")
    return header + payload


def unpack_binary_values(data: bytes) -> list[float]:
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

    def __init__(self) -> None:
        self.buffer = []

    def clear(self) -> None:
        ...  # VISA bus clear

    def read(self, encoding=None) -> str:
        result = self.buffer.pop(0)
        if isinstance(result, bytes):
            return result.decode(encoding)
        return result

    def write(self, message: str) -> int:
        self.buffer.append(message)
        return 1

    def query(self, message: str) -> str:
        self.write(message)
        return self.read()

    def read_bytes(self, count: int) -> bytes:
        return bytes(self.buffer.pop(0))[:count]

    def write_raw(self, message: bytes) -> int:
        self.buffer.append(message)

    def query_binary_values(self, message: str, *, datatype="f", is_big_endian=False):
        self.write(message)
        return unpack_binary_values(self.buffer.pop(0))
