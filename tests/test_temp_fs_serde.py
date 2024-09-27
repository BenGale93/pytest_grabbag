import pickle
import sys

import pytest

from pytest_grabbag import TempFsFactory, _serde
from pytest_grabbag.exceptions import UnsupportedSerializationError


def test_temp_fs_ser_to_pickle(temp_fs_factory: TempFsFactory, func_name) -> None:
    temp_fs = temp_fs_factory.mktemp(func_name)

    test_input = {"test": "content"}
    result = temp_fs.ser("p.pkl", test_input)

    assert pickle.loads(result.read_bytes()) == test_input


def test_temp_fs_ser_to_yaml(temp_fs_factory: TempFsFactory, func_name) -> None:
    temp_fs = temp_fs_factory.mktemp(func_name)

    result = temp_fs.ser("a/b/c.yaml", {"test": "content"})

    assert "a/b/c" in str(result)
    assert result.read_text() == "test: content\n"


def test_temp_fs_ser_to_yml(temp_fs_factory: TempFsFactory, func_name) -> None:
    temp_fs = temp_fs_factory.mktemp(func_name)

    result = temp_fs.ser("a/b/c.yml", {"test": "content"})

    assert "a/b/c" in str(result)
    assert result.read_text() == "test: content\n"


def test_temp_fs_ser_to_toml(temp_fs_factory: TempFsFactory, func_name) -> None:
    temp_fs = temp_fs_factory.mktemp(func_name)

    result = temp_fs.ser("a/b/c.toml", {"test": "content"})

    assert "a/b/c" in str(result)
    assert result.read_text() == 'test = "content"\n'


def test_temp_fs_ser_to_json(temp_fs_factory: TempFsFactory, func_name) -> None:
    temp_fs = temp_fs_factory.mktemp(func_name)

    result = temp_fs.ser("a/b/c.json", {"test": "content"})

    assert "a/b/c" in str(result)
    assert result.read_text() == '{"test": "content"}'


def test_temp_fs_ser_fail(temp_fs_factory: TempFsFactory, func_name) -> None:
    temp_fs = temp_fs_factory.mktemp(func_name)

    with pytest.raises(UnsupportedSerializationError, match=".txt"):
        temp_fs.ser("a.txt", {"test": "content"})


def test_temp_fs_ser_to_yaml_settings(temp_fs_factory: TempFsFactory, func_name) -> None:
    temp_fs = temp_fs_factory.mktemp(func_name)

    temp_fs.set_serde_kwargs(".yaml", indent=4)
    result = temp_fs.ser("a.yaml", {"test": {"content": "content"}})

    assert result.read_text() == "test:\n    content: content\n"

    temp_fs.set_serde_kwargs(".yaml", indent=2)
    result = temp_fs.ser("b.yaml", {"test": {"content": "content"}})

    assert result.read_text() == "test:\n  content: content\n"


def test_settings_only_apply_to_a_single_temp_fs(temp_fs_factory: TempFsFactory, func_name) -> None:
    content = {"test": {"content": "content"}}
    temp_fs = temp_fs_factory.mktemp(func_name)

    temp_fs.set_serde_kwargs(".yaml", indent=4)
    result = temp_fs.ser("a.yaml", content)

    temp_fs2 = temp_fs_factory.mktemp(func_name)
    result2 = temp_fs2.ser("b.yaml", content)

    assert result.read_text() != result2.read_text()


def test_temp_fs_fake_serde_settings(temp_fs_factory: TempFsFactory, func_name) -> None:
    temp_fs = temp_fs_factory.mktemp(func_name)

    with pytest.raises(UnsupportedSerializationError, match=".fake"):
        temp_fs.set_serde_kwargs(".fake", indent=4)


def test_serde_pydantic_base_model(temp_fs_factory: TempFsFactory, func_name) -> None:
    from pydantic import BaseModel

    class A(BaseModel):
        b: int
        c: str

    example = A(b=1, c="test")

    temp_fs = temp_fs_factory.mktemp(func_name)

    result = temp_fs.ser("a.json", example)

    contents = result.read_text()

    assert contents == '{"b": 1, "c": "test"}'

    loaded_example = A.model_validate_json(contents)

    assert example == loaded_example


def test_serde_pydantic_model_root_model(temp_fs_factory: TempFsFactory, func_name) -> None:
    from pydantic import RootModel

    class A(RootModel[dict[str, str]]):
        pass

    example = A({"test": "root"})

    temp_fs = temp_fs_factory.mktemp(func_name)

    result = temp_fs.ser("a.json", example)

    assert result.read_text() == '{"test": "root"}'


def test_serde_pydantic_yaml(temp_fs_factory: TempFsFactory, func_name) -> None:
    from pydantic import BaseModel
    from yaml import Loader, load

    class A(BaseModel):
        b: int
        c: str

    example = A(b=1, c="test")

    temp_fs = temp_fs_factory.mktemp(func_name)

    result = temp_fs.ser("a.yaml", example)

    contents = result.read_text()

    assert contents == "b: 1\nc: test\n"

    loaded_example = A.model_validate(load(contents, Loader=Loader))

    assert example == loaded_example


def test_toml_not_available(monkeypatch):
    with monkeypatch.context() as m:
        m.setitem(sys.modules, "rtoml", None)
        sm = _serde.SerializationManager()
        with pytest.raises(UnsupportedSerializationError, match="toml"):
            sm.get_serializer(".toml")


def test_yaml_not_available(monkeypatch):
    with monkeypatch.context() as m:
        m.setitem(sys.modules, "yaml", None)
        sm = _serde.SerializationManager()
        with pytest.raises(UnsupportedSerializationError, match="yaml"):
            sm.get_serializer(".yaml")
