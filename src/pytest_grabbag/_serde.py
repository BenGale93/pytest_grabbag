"""Utilities for serializing and deserializing data structures."""

import json
import typing as t

from pytest_grabbag.exceptions import UnsupportedSerializationError

SerializerFunction = t.Callable[[t.Any], str]


class Serializer:
    """Class encapsulating a serializer and its kwargs."""

    def __init__(self, func: SerializerFunction) -> None:
        """Initialise a serializer with the specific serialization function."""
        self.func = func
        self.kwargs: dict[str, t.Any] = {}

    def __call__(self, data: t.Any) -> str:
        """Serialize the given data."""
        return self.func(data, **self.kwargs)


class SerializationManager:
    """Class for managing serializers and their settings."""

    _aliases: t.ClassVar[dict[str, str]] = {".yml": ".yaml"}

    def __init__(self) -> None:
        """Initialise the available serializers depending on optional extras."""
        self._serializers: dict[str, Serializer] = {
            ".json": Serializer(json.dumps),
        }
        try:
            import rtoml

            self._serializers[".toml"] = Serializer(rtoml.dumps)
        except ModuleNotFoundError:  # pragma: no cover
            pass
        try:
            import yaml

            self._serializers[".yaml"] = Serializer(yaml.dump)
        except ModuleNotFoundError:  # pragma: no cover
            pass

    def get_serializer(self, extension: str) -> Serializer:
        """Get the desired serializer depending on the file extension."""
        extension = self._aliases.get(extension, extension)
        try:
            return self._serializers[extension]
        except KeyError:
            raise UnsupportedSerializationError(extension) from None

    def set_kwargs(self, extension: str, **kwargs: t.Any) -> None:
        """Set the keyword arguments for a serializer."""
        try:
            self._serializers[extension].kwargs = kwargs
        except KeyError:
            raise UnsupportedSerializationError(extension) from None
