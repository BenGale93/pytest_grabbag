"""This file contains the exception classes used by pytest-grabbag."""


class GrabBagError(Exception):
    """Base exception class for all exceptions in this module."""


class UnsupportedSerializationError(GrabBagError):
    """Exception raised when trying to serialize to an unsupported format."""

    def __init__(self, format_name: str) -> None:
        """Initialise the exception with the invalid format name."""
        super().__init__(
            f"Unsupported serialization format `{format_name}`. "
            "You can add support for yaml and toml by installing the optional extra `serde`"
        )
