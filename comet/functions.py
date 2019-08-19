"""Functions module."""

import itertools

__all__ = ['Range']

class Range(object):
    """Linear range function generator class.

    Range is [begin, end] if last step does not exceed end.

    >>> list(Range(0, 10, 2.5)) # positive ramp
    [0.0, 2.5, 5.0, 7.5, 10.0]
    >>> list(Range(10, 0, -2.5)) # negative ramp
    [10.0, 7.5, 5.0, 2.5, 0.0]
    """

    def __init__(self, begin, end, step=1.0):
        if step == 0.0:
            raise ValueError("function step can't be zero")
        self.__begin = begin
        self.__end = end
        self.__step = step

    def __iter__(self):
        begin = float(self.__begin)
        end = float(self.__end)
        step = float(self.__step)
        test = [end.__gt__, end.__lt__][begin < end and step >= 0.]
        for value in itertools.count(begin, step):
            if test(value):
                break
            yield value
