import pytest

from pytest_grabbag.exceptions import UnsupportedSerializationError


def test_temp_fs_gen_simple(named_temp_fs) -> None:
    named_temp_fs.gen({"a": "test"})

    assert (named_temp_fs / "a").read_text() == "test"


def test_temp_fs_gen_recursive(named_temp_fs) -> None:
    named_temp_fs.gen({"a": {"b": "test"}})

    assert (named_temp_fs / "a" / "b").read_text() == "test"


def test_temp_fs_gen_empty_dict(named_temp_fs) -> None:
    named_temp_fs.gen({"a": {}})

    assert (named_temp_fs / "a").is_dir()


def test_temp_fs_gen_yaml(named_temp_fs) -> None:
    named_temp_fs.gen({"a.yaml": {"test": "content"}})
    assert (named_temp_fs / "a.yaml").read_text() == "test: content\n"


def test_temp_fs_gen_to_any_file_if_string(named_temp_fs):
    named_temp_fs.gen({"test.py": "print('hello world!')"})

    assert (named_temp_fs / "test.py").read_text() == "print('hello world!')"


def test_temp_fs_gen_to_any_file_if_binary(named_temp_fs):
    content = b"0\x00\x00\x00\x00\x00"

    named_temp_fs.gen({"test.exe": content})

    assert (named_temp_fs / "test.exe").read_bytes() == content


def test_temp_fs_gen_to_unrecognised_serde_fails(named_temp_fs):
    with pytest.raises(UnsupportedSerializationError):
        named_temp_fs.gen({"test.py": 0})
