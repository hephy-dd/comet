import qutie as ui

from comet.settings import SettingsMixin
from comet.resource import ResourceMixin
from comet.utils import escape_string, unescape_string

__all__ = ['PreferencesDialog']

class ResourcesTab(ui.Tab, ResourceMixin, SettingsMixin):

    DefaultReadTermination = '\n'
    DefaultWriteTermination = '\n'
    DefaultTimeout = 2000
    DefaultVisaLibrary = '@py'

    def __init__(self):
        super().__init__(title="Resources")
        self.tree = ui.Tree(
            header=("Resource", "Value"),
            selected=self.on_selected,
            double_clicked=self.on_double_clicked,
        )
        self.edit_button = ui.Button(
            text="&Edit",
            enabled=False,
            clicked=self.on_edit
        )
        self.layout = ui.Row(
            self.tree,
            ui.Column(
                self.edit_button,
                ui.Spacer()
            )
        )

    def load(self):
        self.tree.clear()
        for key, resource in self.resources.items():
            item = self.tree.append([key, None])
            item.append(['resource_name', resource.resource_name])
            item.append(['read_termination', resource.read_termination])
            item.append(['write_termination', resource.write_termination])
            item.append(['timeout', resource.timeout])
            item.append(['visa_library', resource.visa_library])

    def store(self):
        pass

    def restore(self):
        pass

    def on_edit(self):
        item = self.tree.current
        if item:
            text = ui.get_text(
                item[1].value
            )
            if text is not None:
                item[1].value = text

    def on_selected(self, value):
        self.edit_button.enabled = value is not None

    def on_double_clicked(self, value, c):
        self.on_edit()

class PreferencesDialog(ui.Dialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(640, 480)
        self.title = "Preferences"
        self.resources_tab = ResourcesTab()
        self.tab_widget = ui.Tabs(
            self.resources_tab
        )
        self.button_box = ui.DialogButtonBox(
            buttons=('restore_defaults', 'close'),
            clicked=self.on_clicked
        )
        self.layout = ui.Column(
            self.tab_widget,
            self.button_box
        )

    def on_clicked(self, value):
        if value == 'close':
            self.on_apply()
            self.close()
        elif value == 'restore_defaults':
            self.on_restore_defaults()

    def on_apply(self):
        pass

    def on_restore_defaults(self):
        pass
