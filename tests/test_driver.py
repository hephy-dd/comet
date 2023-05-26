import pytest


class Resource:

    def __init__(self, buffer):
        self.buffer = buffer

    def clear(self):
        ...  # VISA bus clear

    def read(self):
        return self.buffer.pop(0)

    def write(self, message):
        self.buffer.append(message)

    def query(self, message):
        self.write(message)
        return self.read()


@pytest.fixture
def buffer():
    return []


@pytest.fixture
def resource(buffer):
    return Resource(buffer)
