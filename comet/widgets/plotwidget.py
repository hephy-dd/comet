"""PlotWidget

Overcomming QtChart's limitations for large data series by storing the actual
data in a separate data set attribute. The series itself contains only a sampled
subset of data the original data.

"""

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets, QtChart

from ..dataseries import DataSeries

__all__ = ['ChartView']

milliseconds = 1000.

def toDateTime(seconds):
    """Returns seconds as QDateTime object."""
    return QtCore.QDateTime.fromMSecsSinceEpoch(seconds * milliseconds)

def toSecs(datetime):
    """Returns QDateTime object as seconds."""
    return datetime.toMSecsSinceEpoch() / milliseconds

def toMSecs(seconds):
    """Returns QDateTime object as milli seconds."""
    return seconds * milliseconds

class DataSetMixin:
    """Mixin class to extend data series classes with a dataset attribute."""

    def stretch(self):
        for axis in self.attachedAxes():
            if axis.orientation() == QtCore.Qt.Horizontal:
                self.chart().updateAxis(axis, axis.min(), axis.max())
                break

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

# Ruler

class MarkerGraphicsItem(QtWidgets.QGraphicsRectItem):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__ellipse = QtWidgets.QGraphicsEllipseItem(-7, -7, 13, 13, self)
        self.__ellipse.setPen(QtCore.Qt.red)
        self.__rect = QtWidgets.QGraphicsRectItem(self)
        self.__rect.setBrush(QtCore.Qt.white)
        self.__rect.setPen(QtCore.Qt.transparent)
        self.__rect.setPos(10, -12)
        self.__text = QtWidgets.QGraphicsTextItem(self)
        self.__text.setPos(10, -12)

    def setColor(self, color):
        self.__ellipse.setPen(QtGui.QColor(color))
        #self.__rect.setPen(QtGui.QColor(color))
        self.__text.setDefaultTextColor(QtGui.QColor(color))

    def setLabel(self, label):
        self.__text.setPlainText(label)
        self.__rect.setRect(self.__text.boundingRect())

class RulerGraphicsItem(QtWidgets.QGraphicsRectItem):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__line = QtWidgets.QGraphicsLineItem(self)
        self.__markers = {}
        self.setColor(QtCore.Qt.red)

    def setRuler(self, pos, rect):
        self.__line.setLine(pos.x() - 1, rect.y(), pos.x() - 1, rect.y() + rect.height())

    def setColor(self, color):
        self.__line.setPen(QtGui.QColor(color))

    def setLabel(self, series, index):
        chart = series.chart()
        pos = chart.mapToPosition(series.at(index))
        value = series.at(index)
        visible = series.at(0).x() <= value.x() <= series.at(series.count()-1).x() and self.isVisible()
        if series not in self.__markers:
            self.__markers[series] = MarkerGraphicsItem(self)
        marker = self.__markers.get(series)
        marker.setPos(pos)
        marker.setLabel("{:G} {}".format(value.y(), series.name()))
        marker.setColor(series.color())
        marker.setVisible(visible and chart.plotArea().contains(marker.pos()))

class Toolbar(QtWidgets.QWidget):

    viewAll = QtCore.pyqtSignal()

    toggleRuler = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.setStyleSheet('Toolbar {background-color: transparent;}')
        # View all button
        button = self.addButton(u'\u2b1a')
        button.setToolTip(self.tr("View All"))
        button.clicked.connect(self.viewAll.emit)
        # Toggle ruler button
        button = self.addButton(u'|')
        button.setStyleSheet('QPushButton {color: red;}')
        button.setCheckable(True)
        button.setToolTip("Toggle Ruler")
        button.toggled.connect(self.toggleRuler.emit)

    def buttons(self):
        return self.layout().widgets()

    def addButton(self, text):
        button = QtWidgets.QPushButton(self)
        button.setFixedSize(24, 24)
        button.setText(text)
        self.layout().addWidget(button)
        return button

class Chart(QtChart.QChart):
    """Custom chart class."""

    def __init__(self):
        super().__init__()
        self.setResolution(800)

    def resolution(self):
        return self.__resolution

    def setResolution(self, count):
        self.__resolution = count

    def addValueAxis(self, align):
        return self.addAxis(ValueAxis(), align)

    def addLogValueAxis(self, align):
        return self.addAxis(LogValueAxis(), align)

    def addDateTimeAxis(self, align):
        return self.addAxis(DateTimeAxis(), align)

    def addCategoryAxis(self, align):
        return self.addAxis(CategoryAxis(), align)

    def addBarCategoryAxis(self, align):
        return self.addAxis(BarCategoryAxis(), align)

    def addAxis(self, axis, align):
        def updateAxis(minimum, maximum):
            self.updateAxis(axis, minimum, maximum)
        axis.rangeChanged.connect(updateAxis)
        super().addAxis(axis, align)
        return axis

    def addLineSeries(self, x, y, parent=None):
        return self.addSeries(LineSeries(parent), x, y)

    def addSplineSeries(self, x, y, parent=None):
        return self.addSeries(SplineSeries(parent), x, y)

    def addScatterSeries(self, x, y, parent=None):
        return self.addSeries(ScatterSeries(parent), x, y)

    def addSeries(self, series, x, y):
        super().addSeries(series)
        series.attachAxis(x)
        series.attachAxis(y)
        return series

    def bounds(self):
        """Returns bounding box of all series."""
        series = self.series()
        if len(series):
            minimumX = []
            maximumX = []
            minimumY = []
            maximumY = []
            for series in series:
                if len(series.data()):
                    x, y = series.data().bounds()
                    minimumX.append(x[0])
                    maximumX.append(x[1])
                    minimumY.append(y[0])
                    maximumY.append(y[1])
            if len(minimumX):
                return (min(minimumX),  max(maximumX)), (min(minimumY),  max(maximumY))
        return ((0., 1.), (0., 1.)) # default bounds

    def fitHorizontal(self, bounds=None):
        bounds = self.bounds() if bounds is None else bounds
        self.zoomReset()
        for axis in self.axes(QtCore.Qt.Horizontal):
            if isinstance(axis, QtChart.QDateTimeAxis):
                axis.setRange(toDateTime(bounds[0][0]), toDateTime(bounds[0][1]))
            else:
                axis.setRange(bounds[0][0], bounds[0][1])

    def fitVertical(self, bounds=None):
        bounds = self.bounds() if bounds is None else bounds
        for axis in self.axes(QtCore.Qt.Vertical):
            if isinstance(axis, QtChart.QDateTimeAxis):
                axis.setRange(toDateTime(bounds[1][0]), toDateTime(bounds[1][1]))
            else:
                axis.setRange(bounds[1][0], bounds[1][1])

    def fit(self, bounds=None):
        bounds = self.bounds() if bounds is None else bounds
        self.fitHorizontal(bounds)
        self.fitVertical(bounds)

    @QtCore.pyqtSlot(object, float, float)
    def updateAxis(self, axis, minimum, maximum):
        if axis in self.axes(QtCore.Qt.Horizontal):
            if isinstance(axis, QtChart.QDateTimeAxis):
                minimum = toSecs(minimum)
                maximum = toSecs(maximum)
            for series in self.series():
                if axis in series.attachedAxes():
                    generator = series.data().sample(minimum, maximum, self.resolution())
                    if isinstance(axis, QtChart.QDateTimeAxis):
                        points = (QtCore.QPointF(toMSecs(x), y) for x, y in generator)
                    else:
                        points = (QtCore.QPointF(x, y) for x, y in generator)
                    series.replace(points) # assign a generator object

class ChartView(QtChart.QChartView):
    """Custom chart view class."""

    def __init__(self, parent=None):
        super().__init__(Chart(), parent)
        self.__createToolbar()
        self.chart().layout().setContentsMargins(0, 0, 0, 0)
        self.chart().setBackgroundRoundness(0)
        self.setRulerEnabled(False)
        self.setRubberBand(QtChart.QChartView.RectangleRubberBand)
        self.setRuler(RulerGraphicsItem())
        # Store mouse pressed state
        self.__mousePressed = False

    def __createToolbar(self):
        self.__toolbar = Toolbar(self)
        self.__toolbar.viewAll.connect(self.chart().fit)
        self.__toolbar.toggleRuler.connect(self.setRulerEnabled)
        self.scene().addWidget(self.__toolbar).setPos(0, 0)

    def toolbar(self):
        return self.__toolbar

    def ruler(self):
        return self.__ruler

    def setRuler(self, item):
        self.__ruler = item
        item.setZValue(100)
        self.chart().scene().addItem(item)

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
        ruler.setRuler(pos, rect)
        ruler.setVisible(visible)
        for i, series in enumerate(chart.series()):
            if len(series.data()):
                points = np.array([point.x() for point in series.pointsVector()])
                index = np.abs(points - value.x()).argmin()
                ruler.setLabel(series, index)
        super().mouseMoveEvent(event)
