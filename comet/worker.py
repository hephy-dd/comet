import logging
import time
import traceback

from PyQt5 import QtCore

__all__ = ['Worker', 'WorkerRunnable']

class Worker(QtCore.QObject):
    """Worker base class, derive to implement custom workers."""

    started = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal()

    exceptionOccured = QtCore.pyqtSignal(object)
    """Emitted if exception occures while running, contains the exection."""

    messageChanged = QtCore.pyqtSignal(str)
    messageCleared = QtCore.pyqtSignal()

    progressChanged = QtCore.pyqtSignal(int, int)
    progressHidden = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__isActive = False

    def showMessage(self, message):
        """Show message, emits signal `messageChanged`."""
        logging.info("worker %s message: %s", self, message)
        self.messageChanged.emit(message)

    def clearMessage(self):
        """Clears message, emits signal `messageCleared`."""
        self.messageCleared.emit()

    def showProgress(self, value, maximum):
        """Show progress, emits signal `progressChanged`."""
        logging.info("worker %s progress: %s of %s", self, value, maximum)
        self.progressChanged.emit(value, maximum)

    def hideProgress(self):
        """Hide process, emits sigmal `progressHidden`."""
        self.progressHidden.emit()

    def run(self):
        """Reimplement for custom worker."""
        pass

    def isGood(self):
        """Returns `True` if worker is active."""
        return self.__isActive

    def wait(self, seconds):
        """Wait or until worker is stopped, erperimental."""
        t = time.time() + seconds
        while time.time() < t:
            if not self.isGood():
                break
            time.sleep(.025)

    def start(self):
        """Start worker, usually called by `WorkerRunner` instance."""
        logging.info("started worker %s", self)
        self.__isActive = True
        self.started.emit()
        try:
            self.run()
        except Exception as e:
            logging.error("exception occured in worker %s", self)
            logging.error(traceback.print_exc())
            self.__isActive = False
            self.exceptionOccured.emit(e)
        finally:
            logging.info("finished worker %s", self)
            self.__isActive = False
            self.finished.emit()

    def stop(self):
        """Request stop."""
        self.__isActive = False

class WorkerRunnable(QtCore.QRunnable):
    """Thread pool runner for worker classes."""

    def __init__(self, worker):
        super().__init__()
        self.__worker = worker

    def run(self):
        self.__worker.start()
