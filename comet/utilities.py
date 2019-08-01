"""Utility functions and paths."""

import os
import re

__all__ = ['PACKAGE_PATH', 'make_path', 'make_label', 'make_id']

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

