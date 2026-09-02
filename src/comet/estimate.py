"""Estimate remaining time."""

from collections.abc import Callable
from datetime import timedelta
from time import monotonic

__all__ = ["Estimate"]


class Estimate:
    """Estimate elapsed time, remaining time, and progress.

    Examples:
        >>> eta = Estimate(42)
        >>> for _ in range(42):
        ...     heavy_operation()
        ...     eta.advance()
        ...     print(eta.elapsed)
        ...     print(eta.remaining)
        ...     print(eta.progress)

    Notes:
        Negative totals are treated as zero. Calls to `advance()` after all
        steps have been completed are ignored.
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

        Calls after all steps have been completed are ignored.
        """
        if self._passed >= self._total:
            return
        now = self._clock()
        self._duration += now - self._prev
        self._prev = now
        self._passed += 1

    @property
    def total(self) -> int:
        """Return the total number of steps."""
        return self._total

    @property
    def passed(self) -> int:
        """Return the number of completed steps."""
        return self._passed

    @property
    def average(self) -> timedelta:
        """Return the average duration of completed steps.

        Returns `timedelta(0)` if no steps have been completed.
        """
        if self._passed == 0:
            return timedelta(0)
        return timedelta(seconds=self._duration / self._passed)

    @property
    def elapsed(self) -> timedelta:
        """Return the elapsed time since initialization."""
        return timedelta(seconds=self._clock() - self._start)

    @property
    def remaining(self) -> timedelta:
        """Return the estimated duration of the remaining steps.

        The estimate is based on the average duration of completed steps.
        Returns `timedelta(0)` if no steps have been completed.
        """
        if self._passed == 0:
            return timedelta(0)
        avg = self._duration / self._passed
        return timedelta(seconds=avg * (self._total - self._passed))

    @property
    def progress(self) -> tuple[int, int]:
        """Return progress as `(completed, total)`."""
        return self._passed, self._total
