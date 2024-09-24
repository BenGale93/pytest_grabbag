import pytest

from pytest_grabbag import _dependencies, exceptions


def test_import_optional_fails():
    with pytest.raises(exceptions.MissingExtraError, match="fake"):
        _dependencies.import_optional("not_real", "fake")
