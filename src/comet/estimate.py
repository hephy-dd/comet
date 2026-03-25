"""Estimate remaining time."""

from datetime import timedelta
from time import monotonic
from typing import Callable

__all__ = ["Estimate"]


class Estimate:
    """Estimate elapsed time, remaining time, and progress.

    >>> e = Estimate(42)
    >>> for _ in range(42):
    ...     heavy_operation()
    ...     e.advance()
    ...     print(e.elapsed)
    ...     print(e.remaining)
    ...     print(e.progress)

    Negative totals are treated as zero.
    Calls to `advance()` after completion are ignored.
    """

    def __init__(self, total: int, *, clock: Callable[[], float] = monotonic) -> None:
        self._clock = clock
        self._total: int = max(0, total)
        self._passed: int = 0
        self._duration: float = 0.0
        self._start: float = self._clock()
        self._prev: float = self._start

    def advance(self) -> None:
        """Record completion of one step.

        If all steps are already completed, this call is ignored.
        """
        if self._passed >= self._total:
            return
        now = self._clock()
        self._duration += now - self._prev
        self._prev = now
        self._passed += 1

    @property
    def total(self) -> int:
        """Total number of steps to be processed."""
        return self._total

    @property
    def passed(self) -> int:
        """Number of completed steps."""
        return self._passed

    @property
    def average(self) -> timedelta:
        """Average duration of a completed step.

        Returns `timedelta(0)` until at least one step has been completed.
        """
        if self._passed == 0:
            return timedelta(0)
        return timedelta(seconds=self._duration / self._passed)

    @property
    def elapsed(self) -> timedelta:
        """Elapsed time since start."""
        return timedelta(seconds=self._clock() - self._start)

    @property
    def remaining(self) -> timedelta:
        """Estimated remaining time based on completed steps.

        Returns `timedelta(0)` until at least one step has been completed.
        """
        if self._passed == 0:
            return timedelta(0)
        avg = self._duration / self._passed
        return timedelta(seconds=avg * (self._total - self._passed))

    @property
    def progress(self) -> tuple[int, int]:
        """Current progress as `(completed, total)`."""
        return self._passed, self._total
