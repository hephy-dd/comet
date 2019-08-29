"""Utility functions and paths."""

import contextlib
import os
import re
import sys

__all__ = [
    'PACKAGE_PATH',
    'make_path',
    'make_label',
    'make_id',
    'replace_ext',
    'switch_dir'
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
