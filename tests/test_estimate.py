from comet.estimate import Estimate


def test_estimate_progress():
    e = Estimate(42)
    assert e.count == 42
    assert e.passed == 0
    assert e.progress == (0, 42)
    for i in range(1, 42 + 1):
        e.advance()
        assert e.passed == i
        assert e.progress == (i, 42)
