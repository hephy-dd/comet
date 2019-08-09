"""Utility functions and paths."""

import itertools
import os
import re

__all__ = ['PACKAGE_PATH', 'make_path', 'make_label', 'make_id', 'Range']

PACKAGE_PATH = os.path.abspath(os.path.dirname(__file__))
"""Absolute path to comet package directory."""

def make_path(*args):
    """Constructs an absolute path relative to comet package path.

    >>> make_path('assets', 'sample.txt')
    '/usr/local/lib/python/comet/assets/sample.txt'
    """
    return os.path.join(PACKAGE_PATH, *args)

def make_label(name):
    """Constructs a pretty label from a name or ID.

    >>> make_label('v_max')
    'V max'
    """
    return name.capitalize().replace('_', ' ')

def make_id(name):
    """Constructs a lower case ID string without special characters from any name.

    >>> make_id('NO-body expects the spanish inquisition!')
    'no_body_expects_the_spanish_inquisition'
    """
    return re.sub(r'[^a-z0-9]+', '_', name.lower()).rstrip("_")

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
