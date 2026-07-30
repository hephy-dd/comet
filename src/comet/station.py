from __future__ import annotations

import logging
import os
from collections.abc import Callable, Mapping
from contextlib import AbstractContextManager, ExitStack
from pathlib import Path
from typing import Any, Self, TextIO

import pyvisa
import yaml
from pyvisa.resources.resource import Resource
from schema import And, Optional, Schema, SchemaError, Use

from comet.driver import Driver, driver_factory

__all__ = ["Station"]

Config = dict[str, Any]
ResourceFactory = Callable[[Config], AbstractContextManager[Any]]

logger = logging.getLogger(__name__)

INSTRUMENT_SCHEMA: Schema = Schema(
    {
        Optional("model"): And(str, lambda s: len(s) > 0),
        "resource_name": And(str, lambda s: len(s) > 0),
        Optional("termination"): And(str, lambda s: len(s) > 0),
        Optional("timeout"): And(Use(float), lambda t: t > 0),  # type: ignore
        Optional("visa_library"): str,
    }
)

DEFAULT_CONFIG_FILES: list[str] = ["station.yaml", "station.yml", "station.json"]


def default_resource_factory(config: Config) -> Resource:
    visa_library = config.get("visa_library", "@py")
    rm = pyvisa.ResourceManager(visa_library)
    resource_name = config["resource_name"]
    termination = config.get("termination", "\r\n")
    timeout_ms = int(config.get("timeout", 8.0) * 1000)
    return rm.open_resource(
        resource_name,
        read_termination=termination,
        write_termination=termination,
        timeout=timeout_ms,
    )


def find_filenames(default_filenames: list[str]) -> list[str]:
    """Lookup an orderd list of files and return absolut paths to existing ones."""
    return [
        os.path.abspath(filename)
        for filename in default_filenames
        if os.path.isfile(filename)
    ]


class Station(Mapping):
    def __init__(self, *, resource_factory: ResourceFactory | None = None) -> None:
        """Create an empty Station instance."""
        self.instruments_config: Config = {}
        self._instruments: dict[str, Any] = {}
        self._stack: ExitStack | None = None
        self.resource_factory: ResourceFactory = (
            resource_factory or default_resource_factory
        )

    @classmethod
    def from_config(
        cls, config: Config, *, resource_factory: ResourceFactory | None = None
    ) -> Station:
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
                raise ValueError(
                    f"Invalid configuration for instrument {name!r}: {exc}"
                )

        station = cls(resource_factory=resource_factory)
        station.instruments_config = validated_configs
        return station

    @classmethod
    def from_file(
        cls,
        config_file: str | Path | TextIO | None = None,
        *,
        resource_factory: Callable[[dict[str, Any]], Any] | None = None,
    ) -> Station:
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
                    logger.warning(
                        "Found multiple config files with supported names: %s",
                        ", ".join(found_config_files),
                    )
                    logger.warning("Using %s", config_file)

        if config_file is None:
            default_file_list = ", ".join(
                [f"{file_name!r}" for file_name in DEFAULT_CONFIG_FILES]
            )
            raise ValueError(
                f"No default config file found, must be one of: {default_file_list}"
            )

        with ExitStack() as stack:
            if isinstance(config_file, (str, os.PathLike, Path)):
                file_obj: Any = stack.enter_context(
                    open(config_file, "r", encoding="utf-8")
                )
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
            raise RuntimeError(
                f"{type(self).__name__!r} context is not active, enter context first."
            )
        return self._stack.enter_context(cm)

    def __setattr__(self, name, value):
        """Prevent modifications to instrument attributes once they are set."""
        if "_instruments" in self.__dict__ and name in self.__dict__.get(
            "_instruments", {}
        ):
            raise AttributeError(
                f"Cannot modify read-only instrument attribute {name!r}"
            )
        object.__setattr__(self, name, value)

    def __getattr__(self, name: str) -> Any:
        instruments = self.__dict__.get("_instruments", {})
        try:
            return instruments[name]
        except KeyError:
            raise AttributeError(
                f"{type(self).__name__!r} has no attribute {name!r}"
            ) from None

    def __getitem__(self, name):
        return self._instruments[name]

    def __contains__(self, name):
        return name in self._instruments

    def __iter__(self):
        return iter(self._instruments)

    def __len__(self):
        return len(self._instruments)

    def __enter__(self) -> Self:
        self._stack = ExitStack()

        for name, config in self.instruments_config.items():
            resource = self._stack.enter_context(self.resource_factory(config))
            driver_cls = (
                driver_factory(config["model"]) if "model" in config else Driver
            )
            self._instruments[name] = driver_cls(resource)

        return self

    def __exit__(
        self,
        exc_type: object,
        exc_value: object,
        traceback: object,
    ) -> None:
        if self._stack is not None:
            self._stack.close()

        self._stack = None
        self._instruments.clear()
