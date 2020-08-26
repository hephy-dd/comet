import qutie as ui

from comet.settings import SettingsMixin
from comet.resource import ResourceMixin
from comet.utils import escape_string, unescape_string

__all__ = ['PreferencesDialog']

class PreferencesTab(ui.Tab, SettingsMixin):

    def load(self):
        pass

    def store(self):
        pass

class ResourcesTab(PreferencesTab, ResourceMixin):

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
            ),
            stretch=(1, 0)
        )

    def load(self):
        self.tree.clear()
        resources = self.settings.get('resources') or {}
        for key, resource in self.resources.items():
            item = self.tree.append([key, None])
            d = resources.get(key) or {}
            item.append(['resource_name', d.get('resource_name') or resource.resource_name])
            item.append(['read_termination', escape_string(d.get('read_termination') or resource.options.get('read_termination') or '\n')])
            item.append(['write_termination', escape_string(d.get('write_termination') or resource.options.get('write_termination') or '\n')])
            item.append(['timeout', d.get('timeout') or resource.options.get('timeout') or 2000])
            item.append(['visa_library', d.get('visa_library') or resource.visa_library])
        self.tree.fit()

    def store(self):
        resources = {}
        for item in self.tree:
            resources[item[0].value] = {
                'resource_name': item.children[0][1].value,
                'read_termination': unescape_string(item.children[1][1].value),
                'write_termination': unescape_string(item.children[2][1].value),
                'timeout': int(item.children[3][1].value),
                'visa_library': item.children[4][1].value
            }
        self.settings['resources'] = resources

    def on_edit(self):
        item = self.tree.current
        if item and not item.children:
            text = ui.get_text(
                item[1].value
            )
            if text is not None:
                item[1].value = text

    def on_selected(self, item):
        self.edit_button.enabled = item is not None and not item.children

    def on_double_clicked(self, index, item):
        self.on_edit()

class OperatorsTab(PreferencesTab):

    def __init__(self):
        super().__init__(title="Operators")
        self.operators_list = ui.List(
            selected=self.on_selected,
            double_clicked=self.on_double_clicked,
        )
        self.add_button = ui.Button(
            text="&Add",
            clicked=self.on_add
        )
        self.edit_button = ui.Button(
            text="&Edit",
            enabled=False,
            clicked=self.on_edit
        )
        self.remove_button = ui.Button(
            text="&Remove",
            clicked=self.on_remove
        )
        self.layout = ui.Row(
            self.operators_list,
            ui.Column(
                self.add_button,
                self.edit_button,
                self.remove_button,
                ui.Spacer()
            ),
            stretch=(1, 0)
        )

    def load(self):
        self.operators_list.clear()
        resources = self.settings.get('operators') or []
        for operator in self.settings.get('operators') or []:
            self.operators_list.append(operator)

    def store(self):
        operators = []
        for operator in self.operators_list:
            operators.append(operator.value)
        self.settings['operators'] = operators

    def on_add(self):
        text = ui.get_text("")
        if text:
            self.operators_list.append(text)

    def on_edit(self):
        item = self.operators_list.current
        if item:
            text = ui.get_text(
                item.value
            )
            if text is not None:
                item.value = text

    def on_remove(self):
        item = self.operators_list.current
        if item:
            self.operators_list.remove(item)

    def on_selected(self, item, index):
        enabled = item is not None
        self.edit_button.enabled = enabled
        self.remove_button.enabled = enabled

    def on_double_clicked(self, index, item):
        self.on_edit()

class PreferencesDialog(ui.Dialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(640, 480)
        self.title = "Preferences"
        self.resources_tab = ResourcesTab()
        self.operators_tab = OperatorsTab()
        self.tab_widget = ui.Tabs(
            self.resources_tab,
            self.operators_tab
        )
        self.button_box = ui.DialogButtonBox(
            buttons=('apply', 'cancel'),
            clicked=self.on_clicked
        )
        self.layout = ui.Column(
            self.tab_widget,
            self.button_box
        )

    def on_clicked(self, value):
        if value == 'apply':
            self.on_apply()
        self.close()

    def on_apply(self):
        ui.show_info(
            text="Application restart required for changes to take effect."
        )
        for tab in self.tab_widget:
            tab.store()

    def run(self):
        for tab in self.tab_widget:
            tab.load()
        super().run()
