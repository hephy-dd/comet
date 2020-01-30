import traceback

from PyQt5 import QtWidgets

__all__ = [
    'show_info',
    'show_warning',
    'show_error',
    'show_exception',
    'show_question'
]

class MessageBox(QtWidgets.QMessageBox):
    """Custom message box class."""

    def __init__(self, icon, title, text, details):
        super().__init__(icon, title, text)
        self.setDetailedText(details)
        layout = self.layout()
        layout.addItem(QtWidgets.QSpacerItem(460, 0), layout.rowCount(), 0, 1, layout.columnCount())

def show_info(title, text, details=None):
    dialog = MessageBox(QtWidgets.QMessageBox.Information, title, text, details)
    return dialog.exec_()

def show_warning(title, text, details=None):
    dialog = MessageBox(QtWidgets.QMessageBox.Warning, title, text, details)
    return dialog.exec_()

def show_error(title, text, details=None):
    dialog = MessageBox(QtWidgets.QMessageBox.Critical, title, text, details)
    return dialog.exec_()

def show_exception(exception):
    return show_error("An exception occured", format(exception), details=traceback.format_exc())

def show_question(title, text, details=None):
    """Returns True for yes and False for no."""
    dialog = MessageBox(QtWidgets.QMessageBox.Question, title, text, details)
    dialog.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    return dialog.exec_() == QtWidgets.QMessageBox.Yes
