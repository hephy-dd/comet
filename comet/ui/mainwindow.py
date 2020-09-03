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
            triggered=self.show_preferences
        )
        self.contents_action = ui.Action(
            text="&Contents",
            shortcut="F1",
            triggered=self.show_contents
        )
        self.about_qt_action = ui.Action(
            text="About Qt",
            triggered=self.show_about_qt
        )
        self.about_action = ui.Action(
            text="&About",
            triggered=self.show_about
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
        self.__message_label = ui.Label()
        self.statusbar.append(self.__message_label)
        self.__progress_bar = ui.ProgressBar()
        self.statusbar.append(self.__progress_bar)
        # Dialogs
        self.about_dialog = AboutDialog()
        self.about_dialog.hide()
        self.preferences_dialog = PreferencesDialog()
        self.preferences_dialog.hide()
        # Events
        self.close_event = self.on_close_event
        self.close_request = close_request
        self.resize(800, 600)
        self.hide_message()
        self.hide_progress()

    def show_preferences(self):
        """Show modal preferences dialog."""
        self.preferences_dialog.run()

    def show_contents(self):
        """Open local webbrowser with contets URL."""
        webbrowser.open(self.contents_url)

    def show_about(self):
        """Show modal about dialog."""
        self.about_dialog.run()

    @property
    def about_text(self):
        return self.about_dialog.about_textarea.value

    @about_text.setter
    def about_text(self, value):
        self.about_dialog.about_textarea.value = value

    def show_about_qt(self):
        """Show modal about Qt dialog."""
        ui.qt.QtWidgets.QMessageBox.aboutQt(self.qt)

    @property
    def message_label(self):
        return self.__message_label

    def show_message(self, message):
        """Show status message."""
        self.message_label.text = message
        self.message_label.show()

    def hide_message(self):
        """Hide status message."""
        self.message_label.clear()
        self.message_label.hide()

    @property
    def progress_bar(self):
        return self.__progress_bar

    def show_progress(self, value, maximum):
        """Show progress bar."""
        self.progress_bar.range = 0, maximum
        self.progress_bar.value = value
        self.progress_bar.show()

    def hide_progress(self):
        """Hide progress bar."""
        self.progress_bar.range = 0, 0
        self.progress_bar.value = 0
        self.progress_bar.hide()

    def show_exception(self, exception, tb=None):
        """Raise message box showing exception information."""
        ui.show_exception(exception, tb)
        self.show_message("Error")
        self.hide_progress()

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
