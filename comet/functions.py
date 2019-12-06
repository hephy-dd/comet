"""Functions module."""

import itertools

__all__ = ['Range']

class Range(object):
    """Linear range function generator class.

    Range is bound to [begin, end].

    >>> list(Range(0, 10, 2.5)) # positive ramp
    [0.0, 2.5, 5.0, 7.5, 10.0]
    >>> list(Range(10, 0, -2.5)) # negative ramp
    [10.0, 7.5, 5.0, 2.5, 0.0]
    """

    def __init__(self, begin, end, step):
        self.__begin = float(begin)
        self.__end = float(end)
        self.__step = float(step)

    @property
    def begin(self):
        """Returns begin value."""
        return self.__begin

    @property
    def end(self):
        """Returns end value."""
        return self.__end

    @property
    def step(self):
        """Returns step value."""
        return self.__step

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
