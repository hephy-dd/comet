import QCharted

from qutie.qutie import QtCore
from qutie.qutie import QtGui
from qutie.widget import Widget

__all__ = ['Plot']

AxesTypes = {
    'value': QCharted.ValueAxis,
    'log': QCharted.LogValueAxis,
    'datetime': QCharted.DateTimeAxis,
    'category': QCharted.CategoryAxis,
}

SeriesTypes = {
    'line': QCharted.LineSeries,
    'spline': QCharted.SplineSeries,
    'scatter': QCharted.ScatterSeries,
}

AlignTypes = {
    'top': QtCore.Qt.AlignTop,
    'bottom': QtCore.Qt.AlignBottom,
    'left': QtCore.Qt.AlignLeft,
    'right': QtCore.Qt.AlignRight
}

class Axis:
    """Axis wrapper class provided for convenience."""

    def __init__(self, axis):
        self.qt = axis

    @property
    def text(self):
        return self.qt.titleText()

    @text.setter
    def text(self, value):
        self.qt.setTitleText(value or "")

    @property
    def color(self):
        return self.qt.linePen().color().name()

    @color.setter
    def color(self, value):
        self.qt.setLinePen(QtGui.QColor(value))

class Series:
    """Series wrapper class provided for convenience."""

    def __init__(self, series):
        self.qt = series

    @property
    def text(self):
        return self.qt.name()

    @text.setter
    def text(self, value):
        self.qt.setName(value or "")

    @property
    def color(self):
        return self.qt.pen().color().name()

    @color.setter
    def color(self, value):
        self.qt.setPen(QtGui.QColor(value))

    def append(self, x, y):
        self.qt.data().append(x, y)

    def replace(self, points):
        self.qt.data().replace(points)

    def clear(self):
        self.qt.data().clear()

class Plot(Widget):

    QtClass = QCharted.ChartView

    def __init__(self, axes={}, series={}, legend=None, **kwargs):
        super().__init__(**kwargs)
        self.__axes = {}
        for key, value in axes.items():
            self.add_axis(key, **value)
        self.__series = {}
        for key, value in series.items():
            self.add_series(key, **value)
        self.legend = legend

    def fit(self):
        self.qt.chart().fit()

    def update(self, axis):
        if isinstance(axis, str):
            axis = self.axes.get(axis)
        self.qt.chart().updateAxis(axis.qt, axis.qt.min(), axis.qt.max())

    @property
    def zoomed(self):
        return self.qt.chart().isZoomed()

    @property
    def axes(self):
        return self.__axes.copy()

    def add_axis(self, id, align, type='value', text=None, color=None, categories={}):
        axis = Axis(AxesTypes.get(type)())
        axis.text = text
        if color is not None:
            axis.color = color
        if isinstance(axis.qt, QCharted.CategoryAxis):
            axis.qt.setStartValue(0)
            for key, value in categories.items():
                axis.qt.append(value, key)
        align = AlignTypes.get(align)
        self.qt.chart().addAxis(axis.qt, align)
        self.__axes[id] = axis

    @property
    def series(self):
        return self.__series.copy()

    def add_series(self, id, x, y, type='line', text=None, color=None):
        series = Series(SeriesTypes.get(type)())
        series.text = text
        if color is not None:
            series.color = color
        x_axis = self.__axes.get(x)
        y_axis = self.__axes.get(y)
        self.qt.chart().addSeries(series.qt, x_axis.qt, y_axis.qt)
        self.__series[id] = series

    @property
    def legend(self):
        return self.__legend

    @legend.setter
    def legend(self, position):
        self.__legend = position
        if position not in AlignTypes:
            self.qt.chart().legend().hide()
        else:
            self.qt.chart().legend().show()
            self.qt.chart().legend().setAlignment(AlignTypes.get(position))
