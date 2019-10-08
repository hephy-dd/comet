"""Utility functions and paths."""

import contextlib
import os
import re
import sys
from collections import OrderedDict

__all__ = [
    'PACKAGE_PATH',
    'make_path',
    'make_label',
    'make_id',
    'replace_ext',
    'switch_dir',
    'Collection',
]

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
    >>> make_id('Nobody expects the spanish inquisition!')
    'nobody_expects_the_spanish_inquisition'
    """
    return re.sub(r'[^a-z0-9]+', '_', name.lower()).rstrip('_')

def replace_ext(filename, ext):
    """Replaces a filename extension.
    >>> replace_ext('/tmp/module.py', '.ui')
    '/tmp/module.ui'
    """
    return ''.join((os.path.splitext(filename)[0], ext))

@contextlib.contextmanager
def switch_dir(path):
    """Change the current working directory to the specified path and restore
    the previous location afterwards.
    >>> with switch_dir('/tmp'):
    ...     print(os.getcwd())
    '/tmp'
    >>> print(os.getcwd())
    '/home/user'
    """
    cwd = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(cwd)

class Collection(object):

    def __init__(self, items=None, base=None):
        self.__items = OrderedDict()
        self.__base = base
        if items is not None:
            for key, value in items:
                self.add(key, value)

    def __len__(self):
        return len(self.__items)

    def keys(self):
        return self.__items.keys()

    def values(self):
        return self.__items.values()

    def get(self, key):
        if key not in self.__items:
            raise KeyError("key down not exists '{}'".format(key))
        return self.__items.get(key)

    def add(self, key, value):
        if self.__base is not None:
            if not isinstance(value, self.__base):
                raise TypeError("value must inherit from {}".format(self.__base))
        if key in self.keys():
            raise KeyError("key is already defined: '{}'".format(key))
        self.__items[key] = value

    def __str__(self):
        return format(self.__items)
