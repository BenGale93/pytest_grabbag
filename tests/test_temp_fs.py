import pytest

from pytest_grabbag import TempFs, TempFsFactory
from pytest_grabbag.exceptions import UnsupportedSerializationError


def test_factory_returns_temp_fs(temp_fs_factory: TempFsFactory) -> None:
    temp_fs = temp_fs_factory.mktemp("test_factory_returns_temp_fs")
    assert isinstance(temp_fs, TempFs)


def test_temp_fs_write_file(temp_fs_factory: TempFsFactory) -> None:
    temp_fs = temp_fs_factory.mktemp("test_temp_fs_mk_file")

    result = temp_fs.write("a/b/c", "d")

    assert "a/b/c" in str(result)
    assert result.read_text() == "d"


def test_temp_fs_write_bytes(temp_fs_factory: TempFsFactory) -> None:
    temp_fs = temp_fs_factory.mktemp("test_temp_fs_mk_file")

    result = temp_fs.write("a/b/c", b"d")

    assert "a/b/c" in str(result)
    assert result.read_bytes() == b"d"


def test_temp_fs_ser_to_yaml(temp_fs_factory: TempFsFactory) -> None:
    temp_fs = temp_fs_factory.mktemp("test_temp_fs_ser_to_yaml")

    result = temp_fs.ser("a/b/c.yaml", {"test": "content"})

    assert "a/b/c" in str(result)
    assert result.read_text() == "test: content\n"


def test_temp_fs_ser_fail(temp_fs_factory: TempFsFactory) -> None:
    temp_fs = temp_fs_factory.mktemp("test_temp_fs_ser_to_yaml")

    with pytest.raises(UnsupportedSerializationError, match=".txt"):
        temp_fs.ser("a.txt", {"test": "content"})


def test_temp_fs_gen_simple(temp_fs_factory: TempFsFactory) -> None:
    temp_fs = temp_fs_factory.mktemp("test_temp_fs_gen_simple")

    temp_fs.gen({"a": "test"})

    assert (temp_fs / "a").read_text() == "test"


def test_temp_fs_gen_recursive(temp_fs_factory: TempFsFactory) -> None:
    temp_fs = temp_fs_factory.mktemp("test_temp_fs_gen_recursive")

    temp_fs.gen({"a": {"b": "test"}})

    assert (temp_fs / "a" / "b").read_text() == "test"


def test_temp_fs_gen_empty_dict(temp_fs_factory: TempFsFactory) -> None:
    temp_fs = temp_fs_factory.mktemp("test_temp_fs_gen_recursive")

    temp_fs.gen({"a": {}})

    assert (temp_fs / "a").is_dir()


def test_temp_fs_gen_yaml(temp_fs_factory: TempFsFactory) -> None:
    temp_fs = temp_fs_factory.mktemp("test_temp_fs_gen_yaml")

    temp_fs.gen({"a.yaml": {"test": "content"}})
    assert (temp_fs / "a.yaml").read_text() == "test: content\n"
