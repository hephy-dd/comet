from PyQt5 import QtCore

__all__ = ['Worker']

class Worker(QtCore.QObject):

    started = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal()

    messageChanged = QtCore.pyqtSignal(str)
    progressChanged = QtCore.pyqtSignal(int)

    exceptionOccured = QtCore.pyqtSignal(Exception)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__message = ""
        self.__progress = 0
        self.__stop_request = False

    def message(self):
        return self.__message

    def setMessage(self, message):
        self.__message = message
        self.messageChanged.emit(self.__message)

    def progress(self):
        return self.__progress

    def setProgress(self, percent):
        self.__progress = max(0, min(100, int(percent)))
        self.progressChanged.emit(self.__progress)

    def stopRequest(self):
        self.__stop_request = True

    def isGood(self):
        return self.__stop_request == False

    def run(self):
        pass

    def start(self):
        self.__stop_request = False
        self.started.emit()
        try:
            self.run()
        except Exception as e:
            self.exceptionOccured.emit(e)
        self.__stop_request = False
        self.finished.emit()
