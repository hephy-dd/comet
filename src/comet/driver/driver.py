from abc import ABC


class Driver(ABC):
    """Base class for instrument drivers."""

    def __init__(self, resource) -> None:
        self.resource = resource
