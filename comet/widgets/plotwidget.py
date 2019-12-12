"""PlotWidget

Overcomming QtChart's limitations for large data series by storing the actual
data in a separate data set attribute. The series itself contains only a sampled
subset of data the original data.

"""

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets, QtChart

from ..dataseries import DataSeries

__all__ = ['PlotWidget']

milliseconds = 1000.

def toDateTime(seconds):
    return QtCore.QDateTime.fromMSecsSinceEpoch(seconds * milliseconds)

def toSecs(datetime):
    return datetime.toMSecsSinceEpoch() / milliseconds

def toMSecs(seconds):
    return seconds * milliseconds

def toAlign(align):
    if isinstance(align, str):
        return getattr(QtCore.Qt, 'Align{}'.format(align.lower().title()))
    return align

class DataSetMixin:
    """Mixin class to extend data series classes with a dataset attribute."""

    def data(self):
        try:
            return self.__data
        except AttributeError:
            self.setData(DataSeries())
            return self.__data

    def setData(self, data):
        if isinstance(data, (list, tuple)):
            data = DataSeries(data)
        self.__data = data

# Axes

class ValueAxis(QtChart.QValueAxis):

    pass

class LogValueAxis(QtChart.QLogValueAxis):

    pass

class DateTimeAxis(QtChart.QDateTimeAxis):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Default multi-line label with indented time
        indent = '&#160;' * 6
        self.setFormat('dd-MM-yyyy<br/>{}hh:mm'.format(indent))

class CategoryAxis(QtChart.QCategoryAxis):

    pass

class BarCategoryAxis(QtChart.QBarCategoryAxis):

    pass

# Series

class LineSeries(QtChart.QLineSeries, DataSetMixin):

    pass

class SplineSeries(QtChart.QSplineSeries, DataSetMixin):

     pass

class ScatterSeries(QtChart.QScatterSeries, DataSetMixin):

    pass

class PlotView(QtChart.QChartView):
    """Custom view for chart and ruler."""

    def __init__(self, parent=None):
        super().__init__(parent)
        chart = QtChart.QChart()
        # Reset margin
        chart.layout().setContentsMargins(0, 0, 0, 0)
        # Reset rounded corners
        chart.setBackgroundRoundness(0)
        self.setChart(chart)
        # Rubber band for zoom
        self.setRulerEnabled(False)
        self.setRubberBand(QtChart.QChartView.RectangleRubberBand)
        # Ruler with symbols and labels for series
        self.__ruler = None
        self.__symbols = {}
        self.__labels = {}
        # Store mouse pressed state
        self.__mousePressed = False

    def ruler(self):
        if not self.__ruler:
            self.__ruler = self.chart().scene().addLine(0, 0, 0, 0)
            self.__ruler.setPen(QtGui.QColor(255,0,0))
            self.__ruler.setZValue(100)
        return self.__ruler

    def rulerSymbol(self, series):
        name = series.name()
        if name not in self.__symbols:
            item = self.chart().scene().addEllipse(0, 0, 13, 13)
            item.setZValue(200)
            self.__symbols[name] = item
        return self.__symbols[name]

    def rulerLabel(self, series):
        name = series.name()
        if name not in self.__labels:
            item = self.chart().scene().addText("")
            item.setZValue(300)
            self.__labels[name] = item
        return self.__labels[name]

    def setRulerEnabled(self, enabled):
        self.__setRulerEnabled = enabled

    def isRulerEnabled(self):
        return self.__setRulerEnabled

    def isMousePressed(self):
        return self.__mousePressed

    def mousePressEvent(self, event):
        self.__mousePressed = True
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.__mousePressed = False
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        """Draws ruler and symbols/labels."""
        chart = self.chart()
        # Position in data
        value = chart.mapToValue(event.pos())
        # Position in plot
        pos = chart.mapToScene(event.pos())
        # Plot area
        rect = chart.plotArea()
        # Hise if mouse pressed (else collides with rubber band)
        visible = rect.contains(pos) and self.isRulerEnabled() and not self.isMousePressed()
        ruler = self.ruler()
        ruler.setLine(pos.x() - 1, rect.y(), pos.x() - 1, rect.y() + rect.height())
        ruler.setVisible(visible)
        for i, series in enumerate(chart.series()):
            points = np.array([point.x() for point in series.pointsVector()])
            index = np.abs(points - value.x()).argmin()
            series_visible = series.at(0).x() <= value.x() <= series.at(series.count()-1).x() and visible
            y = chart.mapToPosition(series.at(index)).y()
            x = chart.mapToPosition(series.at(index)).x()
            symbol = self.rulerSymbol(series)
            symbol.setPos(x - 7, y - 7)
            symbol.setPen(ruler.pen())
            symbol.setVisible(series_visible)
            label = self.rulerLabel(series)
            label.setPlainText("{:.3f}".format(series.at(index).y()))
            label.setPos(x + 7, y - 13)
            label.setVisible(series_visible)
            # label.setDefaultTextColor(series.color())
        super().mouseMoveEvent(event)

class PlotWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setResolution(800)
        view = self.__view = PlotView()
        self.__axes = {}
        self.__series = {}

        # View all button
        button = QtWidgets.QPushButton(u'\u2b1a')
        button.setFixedSize(24, 24)
        button.setToolTip("View All")
        button.clicked.connect(self.fit)
        view.scene().addWidget(button).setPos(8, 8)

        # Toggle ruler button
        button = QtWidgets.QPushButton(u'|')
        button.setStyleSheet('QPushButton {color: red;}')
        button.setFixedSize(24, 24)
        button.setCheckable(True)
        button.setToolTip("Toggle Ruler")
        button.clicked.connect(self.toggleRuler)
        view.scene().addWidget(button).setPos(8, 8+24+4)

        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(view, 16, 16)
        self.setLayout(layout)

    def resolution(self):
        return self.__resolution

    def setResolution(self, samples):
        self.__resolution = samples

    def view(self):
        return self.__view

    def chart(self):
        return self.view().chart()

    def legend(self):
        return self.chart().legend()

    def axes(self):
        return self.__axes

    def series(self):
        return self.__series

    def addValueAxis(self, *args, **kwargs):
        return self.addAxis(ValueAxis, *args, **kwargs)

    def addLogValueAxis(self, name, align, color=None):
        return self.addAxis(LogValueAxis, *args, **kwargs)

    def addDateTimeAxis(self, *args, **kwargs):
        return self.addAxis(DateTimeAxis, *args, **kwargs)

    def addCategoryAxis(self, *args, **kwargs):
        return self.addAxis(CategoryAxis, *args, **kwargs)

    def addBarCategoryAxis(self, *args, **kwargs):
        return self.addAxis(BarCategoryAxis, *args, **kwargs)

    def addAxis(self, cls, name, align, color=None):
        axis = cls()
        axis.setTitleText(name)
        def updateAxis(minimum, maximum):
            self.updateAxis(axis, minimum, maximum)
        axis.rangeChanged.connect(updateAxis)
        self.chart().addAxis(axis, toAlign(align))
        if color is not None:
            axis.setLinePenColor(color)
            axis.setLabelsColor(color)
            axis.setTitleBrush(color)
        self.__axes[name] = axis
        return axis

    def addLineSeries(self, *args, **kwargs):
        return self.addSeries(LineSeries, *args, **kwargs)

    def addSplineSeries(self, *args, **kwargs):
        return self.addSeries(SplineSeries, *args, **kwargs)

    def addScatterSeries(self, *args, **kwargs):
        return self.addSeries(ScatterSeries, *args, **kwargs)

    def addSeries(self, cls, name, x, y, data=None, color=None):
        series = cls()
        series.setName(name)
        if data is None:
            data = DataSeries()
        series.setData(data)
        self.chart().addSeries(series)
        if x in self.__axes.values():
            series.attachAxis(x)
        else:
            series.attachAxis(self.__axes.get(x))
        if y in self.__axes.values():
            series.attachAxis(y)
        else:
            series.attachAxis(self.__axes.get(y))
        if color is None:
            series.setPen(series.pen().color()) # Reset pen
        else:
            series.setPen(color)
        self.__series[name] = series
        return series

    def limits(self):
        """Returns bounding box of all series."""
        if len(self.__series):
            minimumX = []
            maximumX = []
            minimumY = []
            maximumY = []
            for series in self.__series.values():
                x, y = series.data().limits()
                minimumX.append(x[0])
                maximumX.append(x[1])
                minimumY.append(y[0])
                maximumY.append(y[1])
            return (min(minimumX),  max(maximumX)), (min(minimumY),  max(maximumY))
        return ((0., 1.), (0., 1.))

    def fitX(self, limits=None):
        limits = limits or self.limits()
        self.chart().zoomReset()
        for axis in self.chart().axes(QtCore.Qt.Horizontal):
            if isinstance(axis, QtChart.QDateTimeAxis):
                axis.setRange(toDateTime(limits[0][0]), toDateTime(limits[0][1]))
            else:
                axis.setRange(limits[0][0], limits[0][1])

    def fitY(self, limits=None):
        limits = limits or self.limits()
        for axis in self.chart().axes(QtCore.Qt.Vertical):
            if isinstance(axis, QtChart.QDateTimeAxis):
                axis.setRange(toDateTime(limits[1][0]), toDateTime(limits[1][1]))
            else:
                axis.setRange(limits[1][0], limits[1][1])

    def fit(self, limits=None):
        limits = limits or self.limits()
        self.fitX(limits)
        self.fitY(limits)

    def toggleRuler(self, checked):
        self.view().setRulerEnabled(checked)

    @QtCore.pyqtSlot(object, float, float)
    def updateAxis(self, axis, minimum, maximum):
        if axis in self.chart().axes(QtCore.Qt.Horizontal):
            if isinstance(axis, QtChart.QDateTimeAxis):
                minimum = toSecs(minimum)
                maximum = toSecs(maximum)
            for series in self.__series.values():
                if axis in series.attachedAxes():
                    generator = series.data().sample(minimum, maximum, self.resolution())
                    if isinstance(axis, QtChart.QDateTimeAxis):
                        points = (QtCore.QPointF(toMSecs(x), y) for x, y in generator)
                    else:
                        points = (QtCore.QPointF(x, y) for x, y in generator)
                    series.replace(points) # assign a generator object
