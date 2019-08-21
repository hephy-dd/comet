"""Demo using continous und triggered workers and buffers with table views.

Measured data is written to `demo.csv` using class `comet.CsvFormatter`.
"""

import random
import time
import sys, os
from collections import OrderedDict

from PyQt5 import QtCore, QtGui, QtWidgets, uic

import comet

class EnvWorker(comet.Worker):

    sampleReady = QtCore.pyqtSignal(object)

    interval = 5
    """Sample interval in seconds."""

    def read(self):
        # Create fake sample
        t = time.time()
        temp = random.uniform(20, 24)
        humid = random.uniform(45, 55)
        comet.logger().info("read environment: time=%.3f temp=%.1f, humid=%.1f", t, temp, humid)
        self.sampleReady.emit(dict(time=t, temp=temp, humid=humid))

    def run(self):
        """Continously collect environment data."""
        while self.isGood():
            self.read()
            self.wait(self.interval)

class MeasWorker(comet.Worker):
    """Worker collecting measurement data."""

    def __init__(self, envBuffer, measBuffer, parent=None):
        super().__init__(parent)
        self.envBuffer = envBuffer
        self.measBuffer = measBuffer

    def readEnv(self):
        env = self.envBuffer.data()
        temp = env.get('temp')[-1]
        humid = env.get('humid')[-1]
        return dict(temp=temp, humid=humid)

    def rampUp(self, maximum):
        self.showProgress(0, maximum)
        # Open output file in append mode
        with open('demo.csv', 'a') as f:
            # Create CSV formatter for buffer
            formatter = comet.CsvFormatter(f, self.measBuffer.keys())
            for i in range(maximum):
                if not self.isGood():
                    return False
                sample = self.readEnv()
                t = time.time()
                voltage = random.random()
                time.sleep(random.uniform(0.5, 1.5)) # simulate blocking communication
                sample['time'] = t
                sample['voltage'] = voltage
                time.sleep(random.uniform(0.5, 1.5)) # simulate blocking communication
                comet.logger().info("measured: time=%.3f voltage=%.3f", t, voltage)
                self.measBuffer.append(sample)
                formatter.write(sample) # append CSV output
                self.showProgress(i + 1, maximum)
        return True

    def run(self):
        self.showMessage("Starting")
        self.rampUp(10)
        if self.isGood():
            self.showMessage("Finished")
            self.showProgress(1, 1)
        else:
            self.showMessage("Aborted")
            self.showProgress(0, 1)

Ui_Demo, DemoBase = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'demo.ui'))

class Demo(DemoBase):
    """Demo widget with controls and table views."""

    startRequest = QtCore.pyqtSignal()
    stopRequest = QtCore.pyqtSignal()
    resetRequest = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_Demo()
        self.ui.setupUi(self)
        # Reset controls
        self.reset()

    def start(self):
        """Request start, emits signal `startRequest`."""
        self.ui.startPushButton.setEnabled(False)
        self.ui.stopPushButton.setEnabled(True)
        self.startRequest.emit()

    def stop(self):
        """Request stop, emits signal `stopRequest`."""
        self.ui.startPushButton.setEnabled(False)
        self.ui.stopPushButton.setEnabled(False)
        self.stopRequest.emit()

    def reset(self):
        """Request reset, emits signal `resetRequest`."""
        self.ui.startPushButton.setEnabled(True)
        self.ui.stopPushButton.setEnabled(False)
        self.resetRequest.emit()

class MainWindow(comet.MainWindow):
    """Main window holding measurement buffers."""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Setup central widget
        demo = Demo(self)
        demo.startRequest.connect(self.start)
        demo.stopRequest.connect(self.stop)
        self.setCentralWidget(demo)

        # Setup environment buffer
        self.envBuffer = comet.Buffer(self)
        self.envBuffer.addChannel('time')
        self.envBuffer.addChannel('temp')
        self.envBuffer.addChannel('humid')

        # Setup measurement buffer
        self.measBuffer = comet.Buffer(self)
        self.measBuffer.addChannel('time')
        self.measBuffer.addChannel('voltage')
        self.measBuffer.addChannel('temp')
        self.measBuffer.addChannel('humid')

        # Setup environment model and view
        model = comet.BufferTableModel(self)
        model.setBuffer(self.envBuffer)
        demo.ui.envTableView.setModel(model)

        # Setup measurement model and view
        model = comet.BufferTableModel(self)
        model.setBuffer(self.measBuffer)
        demo.ui.measTableView.setModel(model)

        # Setup environmental worker
        worker = EnvWorker()
        worker.sampleReady.connect(self.envBuffer.append)
        self.startWorker(worker)

        # Setup measurement worker
        self.worker = MeasWorker(self.envBuffer, self.measBuffer, self)
        self.worker.finished.connect(self.stop)
        self.worker.finished.connect(demo.reset)

        self.showMessage("Ready")

    def start(self):
        """Start measurement."""
        if self.worker.isGood():
            return
        self.measBuffer.clear()
        self.startWorker(self.worker)

    def stop(self):
        """Stop measurement."""
        if self.worker.isGood():
            self.worker.stop()
        while self.worker.isGood():
            self.worker.wait(.25)
        demo = self.centralWidget()
        demo.reset()

def main():
    app = comet.Application()
    window = MainWindow()
    window.show()
    return app.run()

if __name__ == '__main__':
    sys.exit(main())
