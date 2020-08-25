import webbrowser

import qutie as ui

from ..process import ProcessMixin
from ..utils import make_path

from ..ui.preferences import PreferencesDialog
from ..ui.about import AboutDialog

__all__ = ['MainWindow']

class MainWindow(ui.MainWindow, ProcessMixin):

    contents_url = "https://github.com/hephy-dd/comet/"

    def __init__(self, *args, close_request=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Set Icon
        self.icon = make_path('assets', 'icons', 'comet.svg')
        # Actions
        self.quit_action = ui.Action(
            text="&Quit",
            shortcut="Ctrl+Q",
            triggered=self.close
        )
        self.preferences_action = ui.Action(
            text="Prefere&nces",
            triggered=self.showPreferences
        )
        self.contents_action = ui.Action(
            text="&Contents",
            shortcut="F1",
            triggered=self.showContents
        )
        self.about_qt_action = ui.Action(
            text="About Qt",
            triggered=self.showAboutQt
        )
        self.about_action = ui.Action(
            text="&About",
            triggered=self.showAbout
        )
        # Menus
        self.file_menu = self.menubar.append("&File")
        self.file_menu.append(self.quit_action)
        self.edit_menu = self.menubar.append("&Edit")
        self.edit_menu.append(self.preferences_action)
        self.help_menu = self.menubar.append("&Help")
        self.help_menu.append(self.contents_action)
        self.help_menu.append(self.about_qt_action)
        self.help_menu.append(self.about_action)
        # Setup status bar widgets
        self.__messageLabel = ui.Label()
        self.statusbar.append(self.__messageLabel)
        self.__progressBar = ui.ProgressBar()
        self.statusbar.append(self.__progressBar)
        # Dialogs
        self.about_dialog = AboutDialog()
        self.about_dialog.hide()
        self.preferences_dialog = PreferencesDialog()
        self.preferences_dialog.hide()
        # Events
        self.close_event = self.on_close_event
        self.close_request = close_request
        self.resize(800, 600)

    def showPreferences(self):
        """Show modal preferences dialog."""
        self.preferences_dialog.run()

    def showContents(self):
        """Open local webbrowser with contets URL."""
        webbrowser.open(self.contents_url)

    def showAbout(self):
        """Show modal about dialog."""
        self.about_dialog.run()

    def aboutText(self):
        return self.about_dialog.about_textarea.value

    def setAboutText(self, text):
        self.about_dialog.about_textarea.value = text

    def showAboutQt(self):
        """Show modal about Qt dialog."""
        ui.qt.QtWidgets.QMessageBox.aboutQt(self.qt)

    def messageLabel(self):
        return self.__messageLabel

    def showMessage(self, message):
        self.messageLabel().text = message
        self.messageLabel().show()

    def clearMessage(self):
        self.messageLabel().clear()
        self.messageLabel().hide()

    def progressBar(self):
        return self.__progressBar

    def showProgress(self, value, maximum):
        self.progressBar().range = 0, maximum
        self.progressBar().value = value
        self.progressBar().show()

    def hideProgress(self):
        self.progressBar().hide()

    def showException(self, exception):
        """Raise message box showing exception inforamtion."""
        box = QtWidgets.QMessageBox(self)
        box.setIcon(box.Icon.Critical)
        box.setWindowTitle(self.tr("Error"))
        box.setText(format(exception))
        if hasattr(exception, 'details'):
            box.setDetailedText(format(exception.details))
        box.exec_()
        self.showMessage(self.tr("Error"))
        self.hideProgress()

    def on_close_event(self):
        if ui.show_question(
            text="Quit application?"
        ):
            self.emit('close_request')
            if self.processes:
                dialog = ProcessDialog(self.qt)
                dialog.exec_()
            return True
        return False

class ProcessDialog(ui.qt.QtWidgets.QProgressDialog, ProcessMixin):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRange(0, 0)
        self.setValue(0)
        self.setCancelButton(None)
        self.setLabelText("Stopping active threads...")

    def close(self):
        self.processes.stop()
        self.processes.join()
        super().close()

    def exec_(self):
        ui.single_shot(0.250, self.close)
        return super().exec_()
