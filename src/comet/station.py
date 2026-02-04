import os
import logging
from collections.abc import Mapping
from contextlib import ExitStack
from typing import Any, Callable, ContextManager, Optional, TextIO, Union

import pyvisa
import pyvisa.constants
import yaml
from pathlib import Path
from schema import Schema, SchemaError, And, Optional as Opt, Use

from comet.driver import driver_factory, Driver

__all__ = ["Station"]

Config = dict[str, Any]
ResourceFactory = Callable[[Config], ContextManager[Any]]

logger = logging.getLogger(__name__)


INSTRUMENT_SCHEMA: Schema = Schema({
    Opt("model"): And(str, lambda s: len(s) > 0),
    "resource_name": And(str, lambda s: len(s) > 0),
    Opt("baud_rate"): And(Use(int), lambda x: x > 0),
    Opt("data_bits"): And(Use(int), lambda x: x in (5, 6, 7, 8)),
    Opt("parity"): And(Use(str), lambda s: s.lower() in ("none", "odd", "even", "mark", "space")),
    Opt("stop_bits"): And(Use(str), lambda s: s.lower() in ("one", "one_and_a_half", "two")),
    Opt("flow_control"): And(Use(str), lambda s: s.lower() in ("none", "xon_xoff", "rts_cts", "dtr_dsr")),
    Opt("termination"): str,
    Opt("timeout"): And(Use(float), lambda t: t > 0),
    Opt("visa_library"): str,
})

DEFAULT_CONFIG_FILES: list[str] = ["station.yaml", "station.yml", "station.json"]

DEFAULT_BAUD_RATE: int = 9600
DEFAULT_DATA_BITS: int = 8
DEFAULT_PARITY: str = "none"
DEFAULT_STOP_BITS: str = "one"
DEFAULT_FLOW_CONTROL: str = "none"
DEFAULT_TERMINATION: str = "\r\n"
DEFAULT_TIMEOUT: float = 2.0
DEFAULT_VISA_LIBRARY: str = "@py"


def default_resource_factory(config: Config) -> pyvisa.Resource:
    resource_name = config["resource_name"]

    baud_rate = int(config.get("baud_rate", DEFAULT_BAUD_RATE))
    data_bits = int(config.get("data_bits", DEFAULT_DATA_BITS))

    parity = str(config.get("parity", DEFAULT_PARITY)).lower()
    stop_bits = str(config.get("stop_bits", DEFAULT_STOP_BITS)).lower()
    flow_control = str(config.get("flow_control", DEFAULT_FLOW_CONTROL)).lower()

    read_termination = config.get("termination", DEFAULT_TERMINATION)
    write_termination = config.get("termination", DEFAULT_TERMINATION)

    timeout_sec = float(config.get("timeout", DEFAULT_TIMEOUT))
    timeout_ms = int(timeout_sec * 1000)

    visa_library = config.get("visa_library", DEFAULT_VISA_LIBRARY)
    if not visa_library:
        rm = pyvisa.ResourceManager()
    else:
        rm = pyvisa.ResourceManager(visa_library)

    resource = rm.open_resource(resource_name)

    if hasattr(resource, "read_termination"):
        resource.read_termination = read_termination

    if hasattr(resource, "write_termination"):
        resource.write_termination = write_termination

    if hasattr(resource, "timeout"):
        resource.timeout = timeout_ms

    if hasattr(resource, "baud_rate"):
        resource.baud_rate = baud_rate

    if hasattr(resource, "data_bits"):
        resource.data_bits = data_bits

    if hasattr(resource, "parity"):
        if parity == "none":
            resource.parity = pyvisa.constants.Parity.none
        elif parity == "even":
            resource.parity = pyvisa.constants.Parity.even
        elif parity == "odd":
            resource.parity = pyvisa.constants.Parity.odd
        elif parity == "mark":
            resource.parity = pyvisa.constants.Parity.mark
        elif parity == "space":
            resource.parity = pyvisa.constants.Parity.space
        else:
            raise ValueError(f"Invalid parity: {parity}")

    if hasattr(resource, "stop_bits"):
        if stop_bits == "one":
            resource.stop_bits = pyvisa.constants.StopBits.one
        elif stop_bits == "one_and_a_half":
            resource.stop_bits = pyvisa.constants.StopBits.one_and_a_half
        elif stop_bits == "two":
            resource.stop_bits = pyvisa.constants.StopBits.two
        else:
            raise ValueError(f"Invalid stop_bits: {stop_bits}")

    if hasattr(resource, "flow_control"):
        if flow_control == "none":
            resource.flow_control = pyvisa.constants.ControlFlow.none
        elif flow_control == "xon_xoff":
            resource.flow_control = pyvisa.constants.ControlFlow.xon_xoff
        elif flow_control == "rts_cts":
            resource.flow_control = pyvisa.constants.ControlFlow.rts_cts
        elif flow_control == "dtr_dsr":
            resource.flow_control = pyvisa.constants.ControlFlow.dtr_dsr
        else:
            raise ValueError(f"Invalid flow_control: {flow_control}")

    return resource


def find_filenames(default_filenames: list[str]) -> list[str]:
    """Lookup an orderd list of files and return absolut paths to existing ones."""
    return [os.path.abspath(filename) for filename in default_filenames if os.path.isfile(filename)]


class Station(Mapping):
    def __init__(self, *, resource_factory: Optional[ResourceFactory] = None) -> None:
        """Create an empty Station instance."""
        self.instruments_config: Config = {}
        self._instruments: dict[str, Any] = {}
        self._stack: Optional[ExitStack] = None
        self.resource_factory: ResourceFactory = resource_factory or default_resource_factory

    @classmethod
    def from_config(cls, config: Config, *, resource_factory: Optional[ResourceFactory] = None) -> "Station":
        """
        Create a Station instance from a config dictionary.

        Args:
            config: Dictionary with structure like:
                {
                    "instruments": {
                        "name1": { ... },
                        "name2": { ... },
                    }
                }
            resource_factory: Optional custom factory function.
        Returns:
            Configured Station instance (not yet entered).
        """
        instruments = config.get("instruments", {})
        validated_configs = {}

        for name, conf in instruments.items():
            try:
                validated = INSTRUMENT_SCHEMA.validate(conf)
                validated_configs[name] = validated
            except SchemaError as exc:
                raise ValueError(f"Invalid configuration for instrument {name!r}: {exc}")

        station = cls(resource_factory=resource_factory)
        station.instruments_config = validated_configs
        return station

    @classmethod
    def from_file(cls, config_file: Optional[Union[str, Path, TextIO]] = None, *, resource_factory: Optional[Callable[[dict[str, Any]], Any]] = None) -> "Station":
        """
        Create a Station instance from a config file.

        Args:
            config_file: Optional config file name or file like object.
            resource_factory: Optional custom factory function.
        Returns:
            Configured Station instance (not yet entered).
        """
        if config_file is None:
            found_config_files = find_filenames(DEFAULT_CONFIG_FILES)
            if found_config_files:
                config_file = found_config_files[0]
                if len(found_config_files) > 1:
                    logger.warning("Found multiple config files with supported names: %s", ", ".join(found_config_files))
                    logger.warning("Using %s", config_file)

        if config_file is None:
            default_file_list = ", ".join([f"{file_name!r}" for file_name in DEFAULT_CONFIG_FILES])
            raise ValueError(f"No default config file found, must be one of: {default_file_list}")

        with ExitStack() as stack:
            if isinstance(config_file, (str, os.PathLike, Path)):
                file_obj: Any = stack.enter_context(open(config_file, "r", encoding="utf-8"))
            elif hasattr(config_file, "read"):
                file_obj = config_file
            else:
                raise TypeError(f"Unsupported config file type: {config_file!r}")

            config = yaml.safe_load(file_obj)  # YAML is a superset of JSON

        # Default for empty files
        if config is None:
            config = {}

        # Reject arrays
        if not isinstance(config, dict):
            raise TypeError(f"Unsupported config file type: {config_file!r}")

        return cls.from_config(config, resource_factory=resource_factory)

    def add_instrument(self, name: str, /, **kwargs) -> None:
        if name in self.instruments_config:
            raise KeyError(f"Instrument {name!r} already in configuration.")
        self.instruments_config.setdefault(name, {})
        self.update_instrument(name, **kwargs)

    def update_instrument(self, name: str, /, **kwargs):
        if name not in self.instruments_config:
            raise KeyError(f"Instrument {name!r} not found in configuration.")
        conf_dict = self.instruments_config[name]
        conf_dict.update(**kwargs)
        try:
            validated = INSTRUMENT_SCHEMA.validate(conf_dict)
            self.instruments_config[name] = validated
        except SchemaError as e:
            raise ValueError(f"Invalid update for instrument {name!r}: {e}")

    def enter_context(self, cm: Any) -> Any:
        """Enter an context manager and attach it to the station's lifecycle."""
        if not self._stack:
            raise RuntimeError(f"{type(self).__name__!r} context is not active, enter context first.")
        return self._stack.enter_context(cm)

    def __enter__(self) -> "Station":
        self._stack = ExitStack()
        for name, config in self.instruments_config.items():
            # Create resource via factory.
            res_cm = self.resource_factory(config)
            # Open the resource and instantiate the driver.
            res = self._stack.enter_context(res_cm)
            driver_cls = driver_factory(config["model"]) if "model" in config else Driver
            self._instruments[name] = driver_cls(res)
            # Attach as a read-only attribute.
            object.__setattr__(self, name, self._instruments[name])
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Close all instrument resources."""
        if self._stack:
            self._stack.close()
        for name in self._instruments:
            if hasattr(self, name):
                object.__delattr__(self, name)
        self._instruments = {}

    def __setattr__(self, name, value):
        """Prevent modifications to instrument attributes once they are set."""
        if "_instruments" in self.__dict__ and name in self.__dict__.get("_instruments", {}):
            raise AttributeError(f"Cannot modify read-only instrument attribute {name!r}")
        object.__setattr__(self, name, value)

    def __getitem__(self, name):
        return self._instruments[name]

    def __contains__(self, name):
        return name in self._instruments

    def __iter__(self):
        return iter(self._instruments)

    def __len__(self):
        return len(self._instruments)
