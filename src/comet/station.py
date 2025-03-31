import os
import json
import logging
from contextlib import ExitStack
from schema import Schema, And, Use, Optional as Optional_, SchemaError
from typing import Any, Callable, Optional

import pyvisa
import yaml

from comet.driver import driver_factory, Driver

logger = logging.getLogger(__name__)

INSTRUMENT_SCHEMA = Schema({
    Optional_('model'): And(str, lambda s: len(s) > 0),
    'resource_name': And(str, lambda s: len(s) > 0),
    Optional_('termination'): And(str, lambda s: len(s) > 0),
    Optional_('timeout'): And(Use(float), lambda t: t > 0),
    Optional_('visa_library'): str,
})


def default_resource_factory(config: dict[str, Any]) -> pyvisa.Resource:
    visa_library = config.get("visa_library", "@py")
    rm = pyvisa.ResourceManager(visa_library)
    resource_name = config['resource_name']
    termination = config.get('termination', "\r\n")
    timeout_ms = int(config.get('timeout', 8.0) * 1000)
    return rm.open_resource(
        resource_name,
        read_termination=termination,
        write_termination=termination,
        timeout=timeout_ms
    )


def find_default_file(default_files: list[str]) -> Optional[str]:
    default_files = [os.path.abspath(f) for f in default_files]
    found_files = [f for f in default_files if os.path.isfile(f)]
    if not found_files:
        logger.critical("No configuration file found.")
        return
    # Select the file by priority (order in default_files).
    for file in default_files:
        if file in found_files:
            selected_file = file
            break
    extra_files = [f for f in found_files if f != selected_file]
    if extra_files:
        logger.warning(f"Ignored {', '.join(extra_files)} as {selected_file} exists.")
    return selected_file


class Station:
    def __init__(self, *,
        resource_factory: Optional[Callable[[dict[str, Any]], Any]] = None,
        resource_middleware: Optional[list[Callable[[Any, dict[str, Any]], Any]]] = None,
    ) -> None:
        """
        Create an empty Station instance.

        Args:
            config: Dictionary with structure like:
                {
                    "instruments": {
                        "name1": { ... },
                        "name2": { ... },
                    }
                }
            resource_factory: Optional custom factory function.
            resource_middleware: Optional list of middleware functions.
        """
        self.instruments_config: dict[str] = {}
        self.instruments: dict[str] = {}
        self._stack: Optional[ExitStack] = None
        self.resource_factory: Callable = resource_factory or default_resource_factory
        self.resource_middleware: list[Callable] = resource_middleware or []

    @classmethod
    def from_config(cls, config: dict[str, Any], *,
        resource_factory: Optional[Callable[[dict[str, Any]], Any]] = None,
        resource_middleware: Optional[list[Callable[[Any, dict[str, Any]], Any]]] = None,
    ) -> "Station":
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
            resource_middleware: Optional list of middleware functions.

        Returns:
            Configured Station instance (not yet entered).
        """
        instruments = config.get("instruments", {})
        validated_configs = {}

        for name, conf in instruments.items():
            try:
                validated = INSTRUMENT_SCHEMA.validate(conf)
                validated_configs[name] = validated
            except SchemaError as e:
                raise ValueError(f"Invalid configuration for instrument '{name}': {e}")

        station = cls(
            resource_factory=resource_factory,
            resource_middleware=resource_middleware,
        )
        station.instruments_config = validated_configs
        return station

    def load_config(self, config_file: Optional[str] = None) -> None:
        if config_file is None:
            default_files = ["station.yml", "station.yaml", "station.json"]
            config_file = find_default_file(default_files)

        # Load configuration based on file extension.
        if config_file.endswith(('.yml', '.yaml')):
            if yaml is None:
                raise ImportError("PyYAML is required for YAML configuration.")
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
        elif config_file.endswith('.json'):
            with open(config_file, 'r') as f:
                config = json.load(f)
        else:
            raise ValueError("Unsupported config file type.")

        # Validate each instrument's configuration.
        raw_instruments = config.get('instruments', {})
        validated_configs = {}
        for name, conf in raw_instruments.items():
            try:
                validated = INSTRUMENT_SCHEMA.validate(conf)
                # Convert the validated dict into an object for attribute access.
                validated_configs[name] = validated
            except SchemaError as e:
                raise ValueError(f"Invalid configuration for instrument '{name}': {e}")
        self.instruments_config = validated_configs

    def add_instrument(self, name: str, /, **kwargs) -> None:
        if name in self.instruments_config:
            raise KeyError(f"Instrument '{name}' already in configuration.")
        self.instruments_config.setdefault(name, {})
        self.update_instrument(name, **kwargs)

    def update_instrument(self, name: str, /, **kwargs):
        if name not in self.instruments_config:
            raise KeyError(f"Instrument '{name}' not found in configuration.")
        conf_dict = self.instruments_config[name]
        conf_dict.update(**kwargs)
        try:
            validated = INSTRUMENT_SCHEMA.validate(conf_dict)
            self.instruments_config[name] = validated
        except SchemaError as e:
            raise ValueError(f"Invalid update for instrument '{name}': {e}")

    def __enter__(self) -> "Station":
        self._stack = ExitStack()
        for name, config in self.instruments_config.items():
            # Create resource via factory.
            res_cm = self.resource_factory(config)
            # Apply any middleware wrappers.
            for middleware in self.resource_middleware:
                res_cm = middleware(res_cm, config)
            # Open the resource and instantiate the driver.
            res = self._stack.enter_context(res_cm)
            driver_cls = driver_factory(config['model']) if "model" in config else Driver
            self.instruments[name] = driver_cls(res)
            # Attach as a read-only attribute.
            object.__setattr__(self, name, self.instruments[name])
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Close all instrument resources."""
        self._stack.close()

    def __getattr__(self, name):
        """Dynamic lookup of instruments from dictionary."""
        if name in self.instruments:
            return self.instruments[name]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        """Prevent modifications to instrument attributes once they are set."""
        if "instruments" in self.__dict__ and name in self.__dict__.get("instruments", {}):
            raise AttributeError(f"Cannot modify read-only instrument attribute '{name}'")
        object.__setattr__(self, name, value)
