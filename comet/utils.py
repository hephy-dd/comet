from typing import Iterable, List

__all__ = ['combine_matrix']


def combine_matrix(a: Iterable, b: Iterable, *args: Iterable) -> List[str]:
    c = [''.join((x, y)) for x in a for y in b]
    if args:
        return combine_matrix(c, *args)
    return c
