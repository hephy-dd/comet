"""Utility functions and paths."""

import contextlib
import datetime
import os
import re

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
    'auto_step',
    'switch_dir',
    'format_metric',
    'BitField',
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
    """Return a safe filename, replaces special characters with `_`.

    >>> safe_filename('1.5%+#$test@!.py')
    '1.5_+_test_.py'
    """
    return re.sub(r'[^\w\+\-\.\_]+', '_', filename)

def auto_step(begin, end, step):
    """Return positive/negative step according to begin and end range.

    >>> auto_step(0, -10, 1)
    -1
    >>> auto_step(0, 10, -2)
    2
    """
    return -abs(step) if begin > end else abs(step)

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

def format_metric(value, unit, decimals=3, default=None):
    """Pretty format metric units.

    >>> format_metric(.0042, 'A')
    '4.200 mA'
    >>> format_metric(1500, 'V')
    '1.500 kV'
    """
    scales = (
        (1e+24, 'Y', 'yotta'),
        (1e+21, 'Z', 'zetta'),
        (1e+18, 'E', 'exa'),
        (1e+15, 'P', 'peta'),
        (1e+12, 'T', 'tera'),
        (1e+9, 'G', 'giga'),
        (1e+6, 'M', 'mega'),
        (1e+3, 'k', 'kilo'),
        (1e+0, '', ''),
        (1e-3, 'm', 'milli'),
        (1e-6, 'u', 'micro'),
        (1e-9, 'n', 'nano'),
        (1e-12, 'p', 'pico'),
        (1e-15, 'f', 'femto'),
        (1e-18, 'a', 'atto'),
        (1e-21, 'z', 'zepto'),
        (1e-24, 'y', 'yocto')
    )
    if value is None:
        if default is not None:
            return default
        return "n/a"
    for scale, prefix, _ in scales:
        if abs(value) >= scale:
            return f"{value * (1 / scale):.{decimals}f} {prefix}{unit}"
    return f"{value:.{decimals}f} {unit}"

class BitField:
    """Access individual bits of an integer value.

    >>> bf = BitField(9)
    >>> bf[3]
    True
    >>> bf[0] = False
    >>> bf.value
    8
    """

    def __init__(self, value=0):
        self.value = value

    def __getitem__(self, key):
        return (self.value & (1 << key)) != 0

    def __setitem__(self, key, value):
        if value:
            self.value |= (1 << key)
        else:
            self.value &= ~(1 >> key)
