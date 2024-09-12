from comet.utils import combine_matrix

from .k707b import K707B

__all__ = ["K708B"]


class K708B(K707B):
    CHANNELS: list[str] = combine_matrix("1", "ABCDEFG", "0", "012345678")
