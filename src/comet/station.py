import os
import logging
from contextlib import ExitStack
from typing import Any, Callable, Optional, TextIO, Union

import pyvisa
import yaml
from pathlib import Path
from schema import Schema, SchemaError, And, Optional as Opt, Use

from comet.driver import driver_factory, Driver

Config = dict[str, Any]
ResourceFactory = Callable[[Config], Any]

logger = logging.getLogger(__name__)

INSTRUMENT_SCHEMA: Schema = Schema({
    Opt("model"): And(str, lambda s: len(s) > 0),
    "resource_name": And(str, lambda s: len(s) > 0),
    Opt("termination"): And(str, lambda s: len(s) > 0),
    Opt("timeout"): And(Use(float), lambda t: t > 0),
    Opt("visa_library"): str,
})

DEFAULT_CONFIG_FILES: list[str] = ["station.yaml", "station.yml", "station.json"]


def default_resource_factory(config: Config) -> pyvisa.Resource:
    visa_library = config.get("visa_library", "@py")
    rm = pyvisa.ResourceManager(visa_library)
    resource_name = config["resource_name"]
    termination = config.get("termination", "\r\n")
    timeout_ms = int(config.get("timeout", 8.0) * 1000)
    return rm.open_resource(
        resource_name,
        read_termination=termination,
        write_termination=termination,
        timeout=timeout_ms
    )


def find_filenames(default_filenames: list[str]) -> list[str]:
    """Lookup an orderd list of files and return absolut paths to existing ones."""
    return [os.path.abspath(filename) for filename in default_filenames if os.path.isfile(filename)]


class Station:
    def __init__(self, *, resource_factory: Optional[ResourceFactory] = None) -> None:
        """Create an empty Station instance."""
        self.instruments_config: Config = {}
        self.instruments: dict[str, Any] = {}
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
            self.instruments[name] = driver_cls(res)
            # Attach as a read-only attribute.
            object.__setattr__(self, name, self.instruments[name])
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Close all instrument resources."""
        self._stack.close()  # type: ignore

    def __getattr__(self, name):
        """Dynamic lookup of instruments from dictionary."""
        if name in self.instruments:
            return self.instruments[name]
        raise AttributeError(f"{type(self).__name__!r} object has no attribute {name!r}")

    def __setattr__(self, name, value):
        """Prevent modifications to instrument attributes once they are set."""
        if "instruments" in self.__dict__ and name in self.__dict__.get("instruments", {}):
            raise AttributeError(f"Cannot modify read-only instrument attribute {name!r}")
        object.__setattr__(self, name, value)
