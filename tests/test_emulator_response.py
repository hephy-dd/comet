import numpy as np
import pytest

from comet.emulator.response import (
    Response,
    TextResponse,
    BinaryResponse,
    RawResponse,
    make_response,
)


def test_text_response():
    res = TextResponse("Ni!")
    assert res == "Ni!"
    assert res == TextResponse("Ni!")
    assert not res == TextResponse("spam")
    assert res.text == "Ni!"
    assert res.encoding == "ascii"
    assert bytes(res) == "Ni!".encode("ascii")


def test_text_response_latin1():
    res = TextResponse("25°C", encoding="latin-1")
    assert res == "25°C"
    assert res == "25°C".encode("latin-1")
    assert res == TextResponse("25°C", encoding="latin-1")
    assert res.text == "25°C"
    assert res.encoding == "latin-1"
    assert bytes(res) == "25°C".encode("latin-1")


def test_text_response_utf8():
    res = TextResponse("blancmangé", encoding="utf-8")
    assert res == "blancmangé"
    assert not res == TextResponse("blancmangé")
    assert res == TextResponse("blancmangé", encoding="utf-8")
    assert res.text == "blancmangé"
    assert res.encoding == "utf-8"
    assert bytes(res) == "blancmangé".encode("utf-8")


def test_bianry_response():
    res = BinaryResponse("shrubbery".encode("ascii"))
    assert res == "#19shrubbery".encode("ascii")
    assert res == BinaryResponse("shrubbery".encode("ascii"))
    assert not res == BinaryResponse("spam".encode("ascii"))
    assert res.data == "shrubbery".encode("ascii")
    assert bytes(res) == "#19shrubbery".encode("ascii")


def test_bianry_response_pack_real32():
    values = [2.0, 7.0, 4.0, 9.0]

    # big-endian (default)
    res = BinaryResponse.pack_real32(values)
    payload_be = np.asarray(values, dtype=np.dtype(">f4"), order="C").tobytes()
    assert res == b"#216" + payload_be
    assert res == BinaryResponse(payload_be)
    assert res.data == payload_be
    assert bytes(res) == b"#216" + payload_be

    # little-endian
    res_le = BinaryResponse.pack_real32(values, big_endian=False)
    payload_le = np.asarray(values, dtype=np.dtype("<f4"), order="C").tobytes()
    assert res_le == b"#216" + payload_le
    assert res_le == BinaryResponse(payload_le)
    assert res_le.data == payload_le
    assert bytes(res_le) == b"#216" + payload_le


def test_bianry_response_pack_int16():
    values = [1, -2, 300]

    # little-endian (exercise sign handling and non-trivial value)
    res_le = BinaryResponse.pack_int16(values, big_endian=False)
    payload_le = np.asarray(values, dtype=np.dtype("<i2"), order="C").tobytes()
    assert res_le == b"#16" + payload_le
    assert res_le == BinaryResponse(payload_le)
    assert res_le.data == payload_le
    assert bytes(res_le) == b"#16" + payload_le

    # big-endian (default)
    res_be = BinaryResponse.pack_int16(values)
    payload_be = np.asarray(values, dtype=np.dtype(">i2"), order="C").tobytes()
    assert res_be == b"#16" + payload_be
    assert res_be == BinaryResponse(payload_be)
    assert res_be.data == payload_be
    assert bytes(res_be) == b"#16" + payload_be


def test_raw_response():
    res = RawResponse("spam".encode("ascii"))
    assert res == "spam".encode("ascii")
    assert res == RawResponse("spam".encode("ascii"))
    assert not res == RawResponse("wibble".encode("ascii"))
    assert res.data == "spam".encode("ascii")
    assert bytes(res) == "spam".encode("ascii")


def test_make_response():
    res = make_response("Ni!")
    assert isinstance(res, TextResponse)
    res = make_response(TextResponse("wibble"))
    assert isinstance(res, TextResponse)
    res = make_response("tiddle".encode("ascii"))
    assert isinstance(res, BinaryResponse)
    res = make_response(42)
    assert isinstance(res, TextResponse)
    res = make_response(42.0)
    assert isinstance(res, TextResponse)
