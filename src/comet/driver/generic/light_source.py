from abc import abstractmethod

__all__ = ["LightSource"]


class LightSource(Driver):

    @property
    @abstractmethod
    def brightness(self) -> int:
        ...

    @brightness.setter
    @abstractmethod
    def brightness(self, brightness: int) -> None:
        ...

    @property
    @abstractmethod
    def light_enabled(self) -> bool:
        ...

    @light_enabled.setter
    @abstractmethod
    def light_enabled(self, light_enabled: bool) -> None:
        ...