from pytest_grabbag import TempFs, TempFsFactory


def test_factory_returns_temp_fs(temp_fs_factory: TempFsFactory, func_name):
    temp_fs = temp_fs_factory.mktemp(func_name)
    assert isinstance(temp_fs, TempFs)


def test_temp_fs_write_file(temp_fs_factory: TempFsFactory, func_name):
    temp_fs = temp_fs_factory.mktemp(func_name)

    result = temp_fs.write("a/b/c", "d")

    assert "a/b/c" in str(result)
    assert result.read_text() == "d"


def test_temp_fs_write_bytes(temp_fs_factory: TempFsFactory, func_name):
    temp_fs = temp_fs_factory.mktemp(func_name)

    result = temp_fs.write("a/b/c", b"d")

    assert "a/b/c" in str(result)
    assert result.read_bytes() == b"d"
