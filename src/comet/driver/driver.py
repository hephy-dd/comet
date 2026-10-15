from abc import ABC
from typing import Protocol

__all__ = ["Driver", "MessageResource"]


class MessageResource(Protocol):
    def clear(self) -> None: ...
    def read(
        self, termination: str | None = None, encoding: str | None = None
    ) -> str: ...
    def write(
        self, message: str, termination: str | None = None, encoding: str | None = None
    ) -> int: ...
    def query(self, message: str, delay: float | None = None) -> str: ...


class Driver(ABC):
    """Base class for instrument drivers."""

    def __init__(self, resource: MessageResource) -> None:
        self.resource = resource
