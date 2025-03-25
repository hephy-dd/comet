import importlib
import inspect
import types

from .driver import Driver

__all__ = ["driver_factory"]


def find_drivers(module: types.ModuleType) -> list[type[Driver]]:
    """Return all classes of a module derving from class Driver."""
    return [
        obj for _, obj in inspect.getmembers(module, inspect.isclass)
        if issubclass(obj, Driver) and obj is not Driver
    ]


def driver_factory(name: str) -> type[Driver]:
    """Dynamically loads and returns a driver class from the drivers package."""
    module_path = f"{__package__}.{name}"
    module = importlib.import_module(module_path)
    module_name = module.__name__.split(".")[-1]
    for driver_cls in find_drivers(module):
        cls_name = driver_cls.__name__
        if module_name.lower() == cls_name.lower():
            return driver_cls
    raise ImportError(f"Module {module_path!r} does not provide a driver.")
