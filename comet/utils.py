"""Utility functions and paths."""

import contextlib
import datetime
import os
import re
import sys

__all__ = [
    'PACKAGE_PATH',
    'make_path',
    'make_label',
    'make_id',
    'make_iso',
    'escape_string',
    'unescape_string',
    'replace_ext',
    'safe_filename',
    'switch_dir',
]

PACKAGE_PATH = os.path.abspath(os.path.dirname(__file__))
"""Absolute path to comet package directory."""

def make_path(*args):
    """Construct an absolute path relative to comet package path.
    >>> make_path('assets', 'sample.txt')
    '/usr/local/lib/python/comet/assets/sample.txt'
    """
    return os.path.join(PACKAGE_PATH, *args)

def make_label(name):
    """Construct a pretty label from a name or ID.
    >>> make_label('v_max')
    'V max'
    """
    return name.capitalize().replace('_', ' ')

def make_id(name):
    """Construct a lower case ID string without special characters from any name.
    >>> make_id('Nobody expects the spanish inquisition!')
    'nobody_expects_the_spanish_inquisition'
    """
    return re.sub(r'[^a-z0-9]+', '_', name.lower()).rstrip('_')

def make_iso(dt=None):
    """Return filesystem safe ISO date time.

    >>> make_iso()
    '2019-12-24T12-21-42'
    >>> make_iso(1423456789.8)
    '2015-02-09T05-39-49'
    """
    if dt is None:
        dt = datetime.datetime.now()
    if not isinstance(dt, datetime.datetime):
        dt = datetime.datetime.fromtimestamp(dt)
    return dt.replace(microsecond=0).isoformat().replace(':', '-')

def escape_string(s):
    """Return string with encoded escaped special characters.

    >>> escape_string("\r\n")
    '\\r\\n'
    """
    return s.encode('unicode-escape').decode()

def unescape_string(s):
    """Return string with decoded escaped special characters.

    >>> unescape_string("\\r\\n")
    '\r\n'
    """
    return bytes(s, encoding='ascii').decode('unicode-escape')

def replace_ext(filename, ext):
    """Replaces a filename extension.
    >>> replace_ext('/tmp/module.py', '.ui')
    '/tmp/module.ui'
    """
    return ''.join((os.path.splitext(filename)[0], ext))

def safe_filename(filename):
    """Return a safe filename, replaces special characters with `_`."""
    return re.sub(r'[^\w\+\-\.\_]+', '_', filename)

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
