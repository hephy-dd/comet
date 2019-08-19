from ..formatter import Formatter

__all__ = ['HephyDbFormatter']

class HephyDbFormatter(Formatter):

    def __init__(self, target):
        super().__init__(target)
