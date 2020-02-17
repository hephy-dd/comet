import traceback

from PyQt5 import QtWidgets

__all__ = [
    'show_info',
    'show_warning',
    'show_error',
    'show_exception',
    'show_question',
    'filename_open',
    'filenames_open',
    'directory_open',
    'filename_save'
]

class MessageBox(QtWidgets.QMessageBox):
    """Custom message box helper class."""

    def __init__(self, icon, title, text, details):
        super().__init__(icon, title, text)
        self.setDetailedText(details)
        layout = self.layout()
        # Workaround to resize message box
        layout.addItem(QtWidgets.QSpacerItem(460, 0), layout.rowCount(), 0, 1, layout.columnCount())

def show_info(title, text, details=None):
    """Show information message box.

    >>> show_info("Info", "NO-body expects the Spanish Inquisition!")
    """
    dialog = MessageBox(QtWidgets.QMessageBox.Information, title, text, details)
    dialog.exec_()

def show_warning(title, text, details=None):
    """Show warning message box.

    >>> show_warning("Warning", "NO-body expects the Spanish Inquisition!")
    """
    dialog = MessageBox(QtWidgets.QMessageBox.Warning, title, text, details)
    dialog.exec_()

def show_error(title, text, details=None):
    """Show warning message box.

    >>> show_error("Error", "NO-body expects the Spanish Inquisition!")
    """
    dialog = MessageBox(QtWidgets.QMessageBox.Critical, title, text, details)
    dialog.exec_()

def show_exception(exception):
    """Show exception message box including exception stack trace.

    >>> try:
    ...     foo()
    ... except NameError as e:
    ...     show_exception(e)
    """
    show_error(title="An exception occured", text=format(exception), details=traceback.format_exc())

def show_question(title, text, details=None):
    """Show question message box, returns True for yes and False for no.

    >>> show_question("Question", "Fancy a cup of Yorkshire Tea?")
    True
    """
    dialog = MessageBox(QtWidgets.QMessageBox.Question, title, text, details)
    dialog.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    return dialog.exec_() == QtWidgets.QMessageBox.Yes

def filename_open(path=None, filter=None, title=None):
    """Shows a filename selection dialog, returns selected filename path.

    >>> filename_open("/home/user", filter="Text (*.txt)")
    '/home/user/example.txt'
    """
    return QtWidgets.QFileDialog.getOpenFileName(None, title or "Open file", path, filter)[0] or None

def filenames_open(path=None, filter=None, title=None):
    """Shows a multiple filenames selection dialog, returns list of selected
    filename paths.

    >>> filename_open("/home/user", filter="Text (*.txt)")
    ['/home/user/example.txt', '/home/user/another.txt']
    """
    return QtWidgets.QFileDialog.getOpenFileNames(None, title or "Open files", path, filter)[0] or None

def directory_open(path=None, title=None):
    """Shows a multiple filenames selection dialog, returns selected directory
    path.

    >>> filename_open(""/home/user")
    '/tmp'
    """
    return QtWidgets.QFileDialog.getExistingDirectory(None, title or "Open directory", path) or None

def filename_save(path=None, filter=None, title=None):
    """Shows a save filename selection dialog, returns selected filename path.

    >>> filename_save("/home/user/example.txt", filter="Text (*.txt)")
    '/home/user/other.txt
    """
    return QtWidgets.QFileDialog.getSaveFileName(None, title or "Save file", path, filter)[0] or None
