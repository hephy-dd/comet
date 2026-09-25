from comet.emulator.router import tsp
from comet.emulator.router.router import Router


def test_get():
    class Target:
        @tsp.get("smua.source.levelv")
        def level(self):
            return 1.23

    result = Router(Target()).dispatch("print(smua.source.levelv)")

    assert result == 1.23


def test_set():
    class Target:
        @tsp.set("smua.source.output")
        def output(self, value):
            return value

    result = Router(Target()).dispatch("smua.source.output = smua.OUTPUT_ON")

    assert result == "smua.OUTPUT_ON"


def test_call():
    class Target:
        @tsp.call("errorqueue.clear")
        def clear(self):
            return "cleared"

    assert Router(Target()).dispatch("errorqueue.clear()") == "cleared"


def test_call_arguments():
    class Target:
        @tsp.call("foo.bar")
        def bar(self, a, b):
            return a, b

    assert Router(Target()).dispatch("foo.bar(1, 2)") == ("1", "2")
