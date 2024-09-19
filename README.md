# Pytest Grab-Bag

A collection of miscellaneous pytest fixtures and plugins.

## Temporary File System

Inspired by `TmpDir` from `dvc`, `TempFs` is a class that makes creating
temporary directories and files easy. It extends the functionality of pytest's
`tmp_path_factory`.

```python
def test_stuff(temp_fs_factory):
    temp_fs = temp_fs_factory.mktemp("test_root")

    # Create a file with the given content
    new_file = temp_fs.write("file1", "hello world")

    assert "hello world" == new_file.read_text()

    # Serialise an object to a yaml file
    temp_fs.ser("file2.yaml", {"key": "value"})

    # Create multiple files at once, even in sub directories.
    temp_fs.gen({"subdir": {"file1": "hello world", "file2": 42}})
```
