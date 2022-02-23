from comet.utils import combine_matrix

from .k707b import K707B, combine_matrix

__all__ = ['K708B']


class K708B(K707B):

    CHANNELS = combine_matrix('1', 'ABCDEFG', '0', '012345678')
