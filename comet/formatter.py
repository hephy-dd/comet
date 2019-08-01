import os

__all__ = ['Formatter']

class Formatter(object):
    """Data formatter writting to file like objects, inherit to create custom
    data formatters.

    >>> with open('sample.txt', 'w') as f:
    ...     formatter = Formatter(f)
    ...     formatter.write('Hello world!')
    """

    write_terminate = os.linesep

    def __init__(self, target):
        self.__target = target

    @property
    def target(self):
        return self.__target

    def write_header(self):
        """Overwrite to implement custom data header format."""
        pass

    def write(self, data):
        self.target.write()
        if self.write_terminate is not None:
            self.target.write(self.write_terminate)

    def flush(self):
        self.target.flush()

