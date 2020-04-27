"""Functions module."""

import itertools

from .utils import auto_step

__all__ = ['Range']

class Range:
    """Linear range function generator class.

    Range is bound to [begin, end].

    >>> list(Range(0, 10, 2.5)) # positive ramp
    [0.0, 2.5, 5.0, 7.5, 10.0]
    >>> list(Range(10, 0, -2.5)) # negative ramp
    [10.0, 7.5, 5.0, 2.5, 0.0]
    >>> list(Range(0, 4, -1)) # auto corrected step
    [0.0, 1.0, 2.0, 3.0, 4.0]
    """

    def __init__(self, begin, end, step):
        self.__begin = float(begin)
        self.__end = float(end)
        self.__step = auto_step(self.__begin, self.__end, float(step))

    @property
    def begin(self):
        """Return begin value."""
        return self.__begin

    @property
    def end(self):
        """Return end value."""
        return self.__end

    @property
    def step(self):
        """Return auto corrected step value."""
        return self.__step

    @property
    def count(self):
        """Return number of steps."""
        return int(math.ceil(abs(self.begin - self.end) / abs(self.step)))

    @property
    def valid(self):
        """Returns True if linear range is valid."""
        return (self.begin < self.end and self.step > 0) \
            or (self.begin > self.end and self.step < 0)

    def __iter__(self):
        if self.valid:
            for value in itertools.count(self.begin, self.step):
                if self.step > 0 and value >= self.end:
                    yield self.end
                    break
                if self.step < 0 and value <= self.end:
                    yield self.end
                    break
                yield value
