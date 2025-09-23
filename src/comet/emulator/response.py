from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

import numpy as np

__all__ = ["TextResponse", "BinaryResponse", "RawResponse"]


@dataclass
class Response(ABC):
    """Base class for emulator response types."""

    @abstractmethod
    def __bytes__(self) -> bytes: ...


@dataclass(repr=False)
class TextResponse(Response):
    """SCPI text response with optional encoding."""
    text: str
    encoding: str = "ascii"  # SCPI default is ascii

    def __repr__(self) -> str:
        n_chars = len(self.text)
        preview = f"{self.text[:13]}..." if n_chars > 16 else self.text
        return f"<{type(self).__name__} text={preview!r} encoding={self.encoding!r}>"

    def __bytes__(self) -> bytes:
        return self.text.encode(self.encoding)

    def __int__(self) -> int:
        return int(self.text)

    def __float__(self) -> float:
        return float(self.text)

    def __str__(self) -> str:
        return self.text

    def __eq__(self, other: object) -> bool:
        if isinstance(other, TextResponse):
            return (self.text, self.encoding) == (other.text, other.encoding)
        if isinstance(other, str):
            return self.text == other
        if isinstance(other, bytes):
            return bytes(self) == other
        return False


@dataclass(repr=False)
class RawResponse(Response):
    """Generic bytes response."""
    data: bytes

    def __repr__(self) -> str:
        n_bytes = len(self.data)
        preview = self.data[:13] + b"..." if n_bytes > 16 else self.data
        return f"<{type(self).__name__} size={n_bytes!r} data={preview!r}>"

    def __bytes__(self) -> bytes:
        return self.data

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RawResponse):
            return self.data == other.data
        if isinstance(other, bytes):
            return self.data == other
        return False


@dataclass(repr=False)
class BinaryResponse(RawResponse):
    """Binary SCPI block response in format `#<n_chr_size><chr_size><bytes>`."""

    def __bytes__(self) -> bytes:
        n_bytes = len(self.data)
        n_digits = len(str(n_bytes))
        if n_digits > 9:
            raise ValueError(
                f"Invalid SCPI block length {n_bytes}; "
                "must be representable with 1-9 digits."
            )
        header = f"#{n_digits}{n_bytes}".encode("ascii")
        return header + self.data

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BinaryResponse):
            return self.data == other.data
        if isinstance(other, bytes):
            return bytes(self) == other
        return False

    @classmethod
    def pack_real32(cls, data, *, big_endian: bool = True) -> "BinaryResponse":
        """Pack numbers as IEEE-754 float32 in a SCPI binary block."""
        dt = np.dtype(">f4" if big_endian else "<f4")
        payload = np.asarray(data, dtype=dt, order="C").tobytes()
        return cls(payload)

    @classmethod
    def pack_int16(cls, data, *, big_endian: bool = True) -> "BinaryResponse":
        """Pack integers as signed int16 in a SCPI binary block."""
        dt = np.dtype(">i2" if big_endian else "<i2")
        payload = np.asarray(data, dtype=dt, order="C").tobytes()
        return cls(payload)


def make_response(response: Any) -> Response:
    """Helper function to convert various types returned by emulator routes into
    emulator response types.

    >>> make_response("spam")
    <TextResponse text='spam' encoding='ascii'>
    >>> make_response(42)
    <TextResponse text='42' encoding='ascii'>
    >>> make_response(b"shrubbery")
    <BinaryResponse size=9 data=b'shrubbery'>
    """
    if isinstance(response, Response):
        return response
    elif isinstance(response, int):
        return TextResponse(format(response))
    elif isinstance(response, float):
        return TextResponse(format(response))
    elif isinstance(response, str):
        return TextResponse(response)
    elif isinstance(response, bytes):
        return BinaryResponse(response)
    elif isinstance(response, bytearray):
        return BinaryResponse(bytes(response))
    raise TypeError(f"Invalid response type: {type(response)}")
