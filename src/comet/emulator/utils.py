from typing import Any, Callable, Optional, Union

__all__ = ["tsp_print", "tsp_assign", "Error", "Value"]


def tsp_print(route: str) -> str:
    return rf"^print\({route}\)$"


def tsp_assign(route: str) -> str:
    return rf"^{route}\s*\=\s*(.+)$"


class Error:
    """Generic error message container."""

    def __init__(self, code: int, message: str) -> None:
        self.code: int = code
        self.message: str = message


class Value:
    """Value container with input and output mapping for handling emulator state."""

    def __init__(self, default: Any, type_in: Optional[Union[dict, Callable]] = None,
                 type_out: Optional[Union[dict, Callable]] = None) -> None:
        self._value: Any = None
        self.default: Any = default
        self.type_in: Optional[Union[dict, Callable]] = type_in
        self.type_out: Optional[Union[dict, Callable]] = type_out
        self.value = default

    def reset(self) -> None:
        """Reset to default value."""
        self.value = self.default

    @property
    def value(self) -> Any:
        if isinstance(self.type_out, dict):
            return self.type_out[self._value]
        elif callable(self.type_out):
            return self.type_out(self._value)
        return self._value

    @value.setter
    def value(self, value: Any) -> Any:
        if isinstance(self.type_in, dict):
            value = self.type_in[value]
        elif callable(self.type_in):
            value = self.type_in(value)
        self._value = value
