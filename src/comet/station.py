import os
import json
import logging
from contextlib import ExitStack
from typing import Any, Callable, Optional

import pyvisa
import yaml
from schema import Schema, SchemaError, And, Optional as Opt, Use 

from comet.driver import driver_factory, Driver

logger = logging.getLogger(__name__)

INSTRUMENT_SCHEMA: Schema = Schema({
    Opt("model"): And(str, lambda s: len(s) > 0),
    "resource_name": And(str, lambda s: len(s) > 0),
    Opt("termination"): And(str, lambda s: len(s) > 0),
    Opt("timeout"): And(Use(float), lambda t: t > 0),
    Opt("visa_library"): str,
})

DEFAULT_CONFIG_FILES: list[str] = ["station.yml", "station.yaml", "station.json"]


def default_resource_factory(config: dict[str, Any]) -> pyvisa.Resource:
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


def find_default_file(default_files: list[str]) -> Optional[str]:
    """Lookup an orderd list of default files and returns the first found or None."""
    default_files = [os.path.abspath(f) for f in default_files]
    found_files = [f for f in default_files if os.path.isfile(f)]
    if not found_files:
        return None
    # Select the file by priority (order in default_files).
    for file in default_files:
        if file in found_files:
            return file
    return None


class Station:
    def __init__(self, *, resource_factory: Optional[Callable[[dict[str, Any]], Any]] = None) -> None:
        """Create an empty Station instance."""
        self.instruments_config: dict[str, Any] = {}
        self.instruments: dict[str, Any] = {}
        self._stack: Optional[ExitStack] = None
        self.resource_factory: Callable = resource_factory or default_resource_factory

    @classmethod
    def from_config(cls, config: dict[str, Any], *, resource_factory: Optional[Callable[[dict[str, Any]], Any]] = None) -> "Station":
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
    def from_file(cls, config_file: Optional[str] = None, *, resource_factory: Optional[Callable[[dict[str, Any]], Any]] = None) -> "Station":
        """
        Create a Station instance from a config file.

        Args:
            config_file: Optional config file name.
            resource_factory: Optional custom factory function.
        Returns:
            Configured Station instance (not yet entered).
        """
        if config_file is None:
            config_file = find_default_file(DEFAULT_CONFIG_FILES)

        if not config_file:
            default_file_list = ", ".join([f"{file_name!r}" for file_name in DEFAULT_CONFIG_FILES])
            raise ValueError(f"No default config file found, must be one of: {default_file_list}")

        # Load configuration based on file extension.
        if config_file.endswith((".yml", ".yaml")):
            with open(config_file, "r") as f:
                config = yaml.safe_load(f)
        elif config_file.endswith(".json"):
            with open(config_file, "r") as f:
                config = json.load(f)
        else:
            raise ValueError(f"Unsupported config file type: {config_file!r}")

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
