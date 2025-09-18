import pytest

from comet.emulator.emulator import Response, TextResponse, BinaryResponse, RawResponse
from comet.emulator.emulator import make_response


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
    assert not res == "25°C"  # UTF-8
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
