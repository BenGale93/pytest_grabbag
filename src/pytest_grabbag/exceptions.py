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


class MissingExtraError(GrabBagError):
    """Exception raised when trying to use an extra that is not installed."""

    def __init__(self, module_name: str, extra_name: str) -> None:
        """Initialise the exception with the missing extra."""
        super().__init__(
            f"The module `{module_name}` is missing. "
            f"You can install it with `pip install pytest-grabbag[{extra_name}]`"
        )


class UnknownTemplateError(GrabBagError):
    """Exception raised when trying to use an unknown template."""

    def __init__(self, template_name: str) -> None:
        """Initialise the exception with the bad template name."""
        super().__init__(
            f"Unknown copier template `{template_name}`. "
            "The name will be the folder the copier.yml file is found within."
        )
