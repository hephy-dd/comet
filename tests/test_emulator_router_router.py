import pytest

from comet.emulator.router.router import NoRouteError, Router, route


class Matcher:
    def __init__(self, expected):
        self.expected = expected

    def match(self, message):
        if message == self.expected:
            return ()
        return None


def test_dispatch():
    class Target:
        @route(Matcher("foo"))
        def foo(self):
            return "FOO"

    assert Router(Target()).dispatch("foo") == "FOO"


def test_dispatch_arguments():
    class Matcher:
        def match(self, message):
            if message == "foo":
                return ("one", "two")
            return None

    class Target:
        @route(Matcher())
        def foo(self, a, b):
            return a, b

    assert Router(Target()).dispatch("foo") == ("one", "two")


def test_no_route():
    router = Router(object())

    with pytest.raises(NoRouteError):
        router.dispatch("foo")


def test_inherited_route():
    class Base:
        VALUE = "base"

        @route(Matcher("foo"))
        def foo(self) -> str:
            return self.VALUE

    class Child(Base):
        VALUE = "child"

    assert Router(Child()).dispatch("foo") == "child"


def test_overridden_route():
    class Base:
        @route(Matcher("foo"))
        def foo(self) -> str:
            return "base"

    class Child(Base):
        @route(Matcher("foo"))
        def foo(self) -> str:
            return "child"

    assert Router(Child()).dispatch("foo") == "child"


def test_properties_are_not_evaluated():
    class Target:
        def __init__(self):
            self.ready = False

        @property
        def dangerous(self):
            assert self.ready
            return "boom"

        @route(Matcher("foo"))
        def foo(self):
            return "FOO"

    target = Target()

    # Constructing/running the router must not evaluate dangerous.
    assert Router(target).dispatch("foo") == "FOO"
