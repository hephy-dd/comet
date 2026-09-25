from __future__ import annotations

import importlib
import inspect
import logging
from dataclasses import dataclass, field
from typing import Any

from ..utils import parse_model_urn
from .response import Response, make_response
from .router import NoRouteError, Router
from .router.regex import regex

# Backward-compatible name for existing emulators.
message = regex

__all__ = ["Emulator", "Context", "emulator_cls_factory", "message"]

logger = logging.getLogger(__name__)

emulator_registry: dict[str, type[Emulator]] = {}


def emulator_cls_factory(model_urn: str) -> type[Emulator]:
    """Returns emulator class from model specified by URN."""
    module_name: str = parse_model_urn(model_urn)
    key: str = module_name
    if key not in emulator_registry:
        try:
            # Try to load module from global namespace
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            # Package can be None
            if not __package__:
                raise
            # If does not exist, try to load from comet.emulator package
            key = f"{__package__}.{module_name}"
            module = importlib.import_module(key)
        # Iterate over all module class members (local and imported).
        for _, cls in inspect.getmembers(module, inspect.isclass):
            if (
                issubclass(cls, Emulator)
                and cls is not Emulator
                # Make sure class is from module, not an imported one.
                and key == cls.__module__
            ):
                emulator_registry[key] = cls
                break
    if key not in emulator_registry:
        raise RuntimeError(f"Unable to locate emulator module: {module_name}")
    return emulator_registry[key]


@dataclass
class Context:
    options: dict[str, Any] = field(default_factory=dict)


class Emulator:
    def __init__(self, context: Context) -> None:
        self.context = context
        self.router = Router(self)

    def __call__(self, message: str) -> Response | list[Response] | None:
        logger.debug("handle message: %s", message)

        try:
            response = self.router.dispatch(message)
        except NoRouteError:
            return None

        if response is None:
            return None

        if isinstance(response, (list, tuple)):
            return [make_response(res) for res in response]

        return make_response(response)
