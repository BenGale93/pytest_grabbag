from pytest_grabbag import TempFs, TempFsFactory


def test_factory_returns_temp_fs(temp_fs_factory: TempFsFactory, function_name):
    temp_fs = temp_fs_factory.mktemp(function_name)
    assert isinstance(temp_fs, TempFs)


def test_temp_fs_write_file(named_temp_fs):
    result = named_temp_fs.write("a/b/c", "d")

    assert "a/b/c" in str(result)
    assert result.read_text() == "d"


def test_temp_fs_write_bytes(named_temp_fs):
    result = named_temp_fs.write("a/b/c", b"d")

    assert "a/b/c" in str(result)
    assert result.read_bytes() == b"d"


def test_chdir(named_temp_fs):
    with named_temp_fs.chdir():
        assert named_temp_fs.cwd() == named_temp_fs


def test_temp_fs_is_named_correctly(named_temp_fs: TempFs):
    assert named_temp_fs.stem == "test_temp_fs_is_named_correctly"
