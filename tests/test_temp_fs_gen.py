import pytest

from pytest_grabbag import TempFsFactory
from pytest_grabbag.exceptions import UnsupportedSerializationError


def test_temp_fs_gen_simple(temp_fs_factory: TempFsFactory, func_name) -> None:
    temp_fs = temp_fs_factory.mktemp(func_name)

    temp_fs.gen({"a": "test"})

    assert (temp_fs / "a").read_text() == "test"


def test_temp_fs_gen_recursive(temp_fs_factory: TempFsFactory, func_name) -> None:
    temp_fs = temp_fs_factory.mktemp(func_name)

    temp_fs.gen({"a": {"b": "test"}})

    assert (temp_fs / "a" / "b").read_text() == "test"


def test_temp_fs_gen_empty_dict(temp_fs_factory: TempFsFactory, func_name) -> None:
    temp_fs = temp_fs_factory.mktemp(func_name)

    temp_fs.gen({"a": {}})

    assert (temp_fs / "a").is_dir()


def test_temp_fs_gen_yaml(temp_fs_factory: TempFsFactory, func_name) -> None:
    temp_fs = temp_fs_factory.mktemp(func_name)

    temp_fs.gen({"a.yaml": {"test": "content"}})
    assert (temp_fs / "a.yaml").read_text() == "test: content\n"


def test_temp_fs_gen_to_any_file_if_string(temp_fs_factory: TempFsFactory, func_name):
    temp_fs = temp_fs_factory.mktemp(func_name)

    temp_fs.gen({"test.py": "print('hello world!')"})

    assert (temp_fs / "test.py").read_text() == "print('hello world!')"


def test_temp_fs_gen_to_unrecognised_serde_fails(temp_fs_factory: TempFsFactory, func_name):
    temp_fs = temp_fs_factory.mktemp(func_name)

    with pytest.raises(UnsupportedSerializationError):
        temp_fs.gen({"test.py": 0})
