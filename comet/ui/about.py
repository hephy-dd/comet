import qutie as ui

from ..version import __version__
from ..utils import make_path

__all__ = ['AboutDialog']

class AboutDialog(ui.Dialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(400, 300)
        self.title = "About"
        self.icon_label = ui.Label(width=48, height=48)
        self.icon_label.pixmap = ui.Pixmap(filename=make_path('assets', 'icons', 'comet.svg'))
        self.icon_label.qt.setScaledContents(True)
        self.title_label = ui.Label(f"COMET {__version__}")
        self.title_label.stylesheet = 'QLabel{font-size: 18px; font-weight: bold; }'
        self.caption_label = ui.Label("Control and Measurement Toolkit")
        self.about_textarea = ui.TextArea(
            value="A COMET application.",
            readonly=True
        )
        self.about_tab = ui.Tab(
            title="&About",
            layout=self.about_textarea
        )
        self.authors_textarea = ui.TextArea(
            value="Bernhard Arnold <bernhard.arnold@oeaw.ac.at>",
            readonly=True
        )
        self.authors_tab = ui.Tab(
            title="A&uthors",
            layout=self.authors_textarea
        )
        self.tab_widget = ui.Tabs(
            self.about_tab,
            self.authors_tab
        )
        self.layout = ui.Column(
            ui.Row(
                self.icon_label,
                ui.Column(
                    self.title_label,
                    self.caption_label
                )
            ),
            self.tab_widget
        )
