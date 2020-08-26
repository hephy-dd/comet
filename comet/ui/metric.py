import qutie as ui

__all__ = ['Metric']

class MetricUnit:

    def __init__(self, base, prefix, name):
        self.base = base
        self.prefix =prefix
        self.name = name

class MetricUnits:

    class Metric:

        def __init__(self, base, prefix, name):
            self.base = base
            self.prefix = prefix
            self.name = name

    default_unit = MetricUnit(1e+0, '', '')
    metric_units = (
        MetricUnit(1e+24, 'Y', 'yotta'),
        MetricUnit(1e+21, 'Z', 'zetta'),
        MetricUnit(1e+18, 'E', 'exa'),
        MetricUnit(1e+15, 'P', 'peta'),
        MetricUnit(1e+12, 'T', 'tera'),
        MetricUnit(1e+9, 'G', 'giga'),
        MetricUnit(1e+6, 'M', 'mega'),
        MetricUnit(1e+3, 'k', 'kilo'),
        default_unit,
        MetricUnit(1e-3, 'm', 'milli'),
        MetricUnit(1e-6, 'u', 'micro'),
        MetricUnit(1e-9, 'n', 'nano'),
        MetricUnit(1e-12, 'p', 'pico'),
        MetricUnit(1e-15, 'f', 'femto'),
        MetricUnit(1e-18, 'a', 'atto'),
        MetricUnit(1e-21, 'z', 'zepto'),
        MetricUnit(1e-24, 'y', 'yocto')
    )

    @classmethod
    def get(cls, value):
        for mertric in cls.metric_units:
            if value >= mertric.base:
                return mertric
        return cls.default_unit

class MetricItem:
    """Metric item used for combo box selection."""

    def __init__(self, metric, unit):
        self.metric = metric
        self.unit = unit

    def __str__(self):
        return f"{self.metric.prefix}{self.unit}"

class Metric(ui.Row):
    """Metric input."""

    default_prefixes = 'YZEPTGMk1munpfazy'

    def __init__(self, unit, *args, value=None, minimum=None, maximum=None,
                 decimals=None, prefixes=None, changed=None,
                 editing_finished=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.__number = ui.Number(minimum=minimum, maximum=maximum, adaptive=True)
        self.__combobox = ui.ComboBox()
        self.unit = unit
        self.decimals = decimals or 0
        self.prefixes = prefixes or self.default_prefixes
        self.value = value or 0.0
        self.append(self.__number)
        self.append(self.__combobox)
        self.stretch = 1, 0
        self.__number.changed = lambda _: self.emit('changed', self.value)
        self.__number.editing_finished = lambda: self.emit('editing_finished')
        self.__combobox.changed = lambda _: self.emit('changed', self.value)
        self.changed = changed
        self.editing_finished = editing_finished

    @property
    def value(self):
        return self.__number.value * self.__combobox.current.metric.base

    @value.setter
    def value(self, value):
        metric = MetricUnits.get(value)
        for item in self.__combobox:
            if item.metric.base == metric.base:
                self.__combobox.current = item
        self.__number.value = value / self.__combobox.current.metric.base

    @property
    def decimals(self):
        return self.__number.decimals

    @decimals.setter
    def decimals(self, value):
        self.__number.decimals = value

    @property
    def unit(self):
        return self.__unit

    @unit.setter
    def unit(self, value):
        self.__unit = value

    @property
    def prefixes(self):
        return [value.metric.prefix for value in self.__combobox.items]

    @prefixes.setter
    def prefixes(self, value):
        self.__combobox.clear()
        for metric in MetricUnits.metric_units:
            if metric.prefix and metric.prefix in value:
                self.__combobox.append(MetricItem(metric, self.__unit))
            elif '1' in value:
                self.__combobox.append(MetricItem(metric, self.__unit))

    @property
    def changed(self):
        return self.__changed

    @changed.setter
    def changed(self, value):
        self.__changed = value

    @property
    def editing_finished(self):
        return self.__editing_finished

    @editing_finished.setter
    def editing_finished(self, value):
        self.__editing_finished = value
