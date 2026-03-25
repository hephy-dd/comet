from datetime import timedelta

from comet.estimate import Estimate


def test_initial_state():
    e = Estimate(5)
    assert e.total == 5
    assert e.passed == 0
    assert e.progress == (0, 5)
    assert e.average == timedelta(0)
    assert e.remaining == timedelta(0)


def test_negative_total_becomes_zero():
    e = Estimate(-3)
    assert e.total == 0
    assert e.progress == (0, 0)
    assert e.remaining == timedelta(0)


def test_advance_increments_passed():
    e = Estimate(3)
    e.advance()
    assert e.passed == 1
    assert e.progress == (1, 3)


def test_advance_stops_at_total():
    e = Estimate(2)
    e.advance()
    e.advance()
    e.advance()  # should be ignored
    assert e.passed == 2
    assert e.progress == (2, 2)


def test_remaining_never_negative():
    e = Estimate(1)
    e.advance()
    e.advance()  # ignored
    assert e.remaining >= timedelta(0)


def test_average_and_remaining_progression():
    e = Estimate(2)

    # before any work
    assert e.average == timedelta(0)
    assert e.remaining == timedelta(0)

    e.advance()
    avg_after_first = e.average
    assert avg_after_first > timedelta(0)
    assert e.remaining >= timedelta(0)

    e.advance()
    assert e.remaining == timedelta(0)


def test_elapsed_increases():
    e = Estimate(1)
    first = e.elapsed
    e.advance()
    second = e.elapsed
    assert second >= first


def test_progress_tuple():
    e = Estimate(4)
    e.advance()
    e.advance()
    assert e.progress == (2, 4)
