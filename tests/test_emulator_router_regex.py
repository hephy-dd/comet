from comet.emulator.router.regex import regex
from comet.emulator.router.router import Router


def test_regex():
    class Target:
        @regex(r"foo")
        def foo(self):
            return "FOO"

    assert Router(Target()).dispatch("foo") == "FOO"


def test_regex_groups():
    class Target:
        @regex(r"set (.+)")
        def set_value(self, value):
            return value

    assert Router(Target()).dispatch("set 123") == "123"


def test_regex_uses_match_semantics():
    class Target:
        @regex(r"foo")
        def foo(self):
            return "FOO"

    assert Router(Target()).dispatch("foobar") == "FOO"


def test_regex_question_mark():
    class Target:
        @regex(r"\*IDN\?$")
        def idn(self):
            return "instrument"

    assert Router(Target()).dispatch("*IDN?") == "instrument"


def test_identity_inheritance():
    class Base:
        IDENTITY = "base"

        @regex(r"\*IDN\?$")
        def idn(self):
            return self.IDENTITY

    class Child(Base):
        IDENTITY = "child"

    assert Router(Child()).dispatch("*IDN?") == "child"
