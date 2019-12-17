import numpy as np

import math
import threading

__all__ = ['DataSeries']

class DataSeries:
    """2D data series using numpy arrays.

    >>> series = DataSeries([(0, 1), (2, 3)])
    >>> series.append(4, 5)
    >>> series.replace([(2, 3), (4, 5), (6, 7)])
    >>> series.bounds()
    ((2, 3), (6, 7))
    """

    def __init__(self, data=None):
        self._lock = threading.RLock()
        self.clear()
        if data is not None:
            self.replace(data)

    def clear(self):
        with self._lock:
            self._x = np.array([])
            self._y = np.array([])

    def append(self, x, y):
        with self._lock:
            self._x = np.append(self._x, x)
            self._y = np.append(self._y, y)

    def replace(self, points):
        with self._lock:
            assert isinstance(points, (list, tuple))
            if len(points):
                points = zip(*points)
                self._x = np.array(next(points))
                self._y = np.array(next(points))
            else:
                self.clear()

    def first(self):
        with self._lock:
            return self._x[0], self._y[0]

    def last(self):
        with self._lock:
            return self._x[-1], self._y[-1]

    def at(self, index):
        with self._lock:
            return self._x[index], self._y[index]

    def xpos(self, value):
        """Returns nearest index for value on ordered series on x axis."""
        with self._lock:
            return np.abs(self._x - value).argmin()

    def bounds(self):
        with self._lock:
            return (self._x[0], self._x[-1]), (np.amin(self._y), np.amax(self._y))

    def sample(self, begin, end, count):
        """Returns a sampling generator, up to `count` samples between `begin` and `end`.

        >>> series = DataSeries()
        >>> list(series.sample(100, 200, 25))
        [...]
        """
        with self._lock:
            assert begin <= end
            assert count > 0
            size = self._x.size
            if size < 1:
                return iter([])
            begin_index = max(0, self.xpos(begin) - 1)
            end_index = min(size - 1, self.xpos(end) + 1)
            step = int(max(1, math.ceil((end_index - begin_index) / count)))
            for i in range(count):
                if begin_index >= end_index:
                    yield self.at(end_index)
                    break
                yield self.at(begin_index)
                begin_index += step

    def __len__(self):
        return self._x.size
