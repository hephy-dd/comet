from .utils import to_unit

__all__ = ["inspect_parameters", "Parameter", "ParameterBase"]


def inspect_parameters(cls):
    """Retrun dictionary of assigned class parameters."""
    parameters = {}
    for mro_cls in cls.__mro__:
        for key, value in mro_cls.__dict__.items():
            if key not in parameters:
                if isinstance(value, Parameter):
                    parameters[key] = value
    return parameters


class Parameter:
    """Class parameter specification."""

    def __init__(self, default=None, *, type=None, minimum=None, maximum=None, choice=None, unit=None, constraint=None):
        self.type = type
        self.minimum = minimum
        self.maximum = maximum
        self.choice = choice
        self.unit = unit
        self.constraint = constraint
        if default is not None:
            default = self.validate(default)
        self.default = default

    @property
    def required(self):
        return self.default is None

    def validate(self, value):
        if self.choice is not None:
            if value not in self.choice:
                raise ValueError(f"not allowed: {repr(value)}, musst be one of: {repr(self.choice)}")
        if self.unit is not None:
            value = to_unit(value, self.unit)
        if self.type is not None:
            value = self.type(value)
        if self.minimum is not None:
            if value < self.minimum:
                raise ValueError(f"out of bounds: {repr(value)}")
        if self.maximum is not None:
            if value > self.maximum:
                raise ValueError(f"out of bounds: {repr(value)}")
        if self.constraint is not None:
            if not self.constraint(self, value):
                raise ValueError(f"failed constraint check: {repr(value)}")
        return value


class ParameterBase:
    """Base class for parameters."""

    def __init__(self, values: dict = None) -> None:
        self.__values = {}
        self.update_parameters(values or {})

    def __getattribute__(self, name):
        parameters = inspect_parameters(type(self))
        if name in parameters:
            default = parameters.get(name).default
            return self.__values.get(name, default)
        return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if name in inspect_parameters(type(self)):
            raise AttributeError(f"can't set parameter: {repr(name)}")
        super().__setattr__(name, value)

    @property
    def parameters(self) -> dict:
        """Retrun dictionary containing all parameter values."""
        values = {}
        for key, value in inspect_parameters(type(self)).items():
            values[key] = getattr(self, key)
        return values

    def update_parameters(self, values: dict) -> None:
        """Update parameter values using a dictionary."""
        parameters = inspect_parameters(type(self))

        # Check for unset required parameters
        required_keys = [key for key, value in parameters.items() if value.required]
        for key in required_keys:
            if key not in self.__values and key not in values:
                raise KeyError(f"missing required parameter: {repr(key)}")

        # Collect new parameter values
        validated_values = {}
        for key, value in values.items():
            parameter = parameters.get(key)
            if parameter is None:
                raise KeyError(f"no such parameter: {repr(key)}")
            validated_values[key] = parameter.validate(value)
        self.__values.update(validated_values)
