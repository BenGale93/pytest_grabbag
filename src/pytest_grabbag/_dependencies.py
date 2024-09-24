import typing as t
from importlib import import_module

from pytest_grabbag.exceptions import MissingExtraError


def import_optional(module_name: str, extra_name: str) -> t.Any:
    try:
        module = import_module(module_name)
    except ImportError:
        raise MissingExtraError(module_name, extra_name) from None

    return module
