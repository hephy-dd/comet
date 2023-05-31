import pytest


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


@pytest.fixture
def resource():
    return MockResource()
