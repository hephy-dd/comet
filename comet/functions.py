"""Functions module."""

import itertools

__all__ = ['Range']

def auto_step(begin, end, step):
    """Return positive/negative step according to begin and end value."""
    return -abs(step) if begin > end else abs(step)

class Range:
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
        self.__step = auto_step(float(step))

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
        """Return step value."""
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
        if not self.valid:
            raise ValueError()
        for value in itertools.count(self.begin, self.step):
            if self.step > 0 and value >= self.end:
                yield self.end
                break
            if self.step < 0 and value <= self.end:
                yield self.end
                break
            yield value
