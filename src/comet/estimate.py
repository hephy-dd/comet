"""Estimate remaining time."""

from datetime import datetime, timedelta

__all__ = ["Estimate"]


class Estimate:
    """Estimate remaining time and progress.

    >>> e = Estimate(42)
    >>> for i in range(42):
    ...     heavy_operation()
    ...     e.advance()
    ...     print(e.elapsed)
    ...     print(e.remaining)
    ...     print(e.progress)
    """

    def __init__(self, total: int) -> None:
        self._total: int = total
        self._deltas: list[timedelta] = []
        self._start: datetime = datetime.now()
        self._prev: datetime = datetime.now()

    def advance(self) -> None:
        now = datetime.now()
        self._deltas.append(now - self._prev)
        self._prev = now

    @property
    def total(self) -> int:
        return self._total

    @property
    def passed(self) -> int:
        return len(self._deltas)

    @property
    def average(self) -> timedelta:
        return sum(self._deltas, timedelta(0)) / max(1, len(self._deltas))

    @property
    def elapsed(self) -> timedelta:
        return datetime.now() - self._start

    @property
    def remaining(self) -> timedelta:
        return max(timedelta(0), (self.average * self.total) - self.elapsed)

    @property
    def progress(self) -> tuple[int, int]:
        return self.passed, self.total
