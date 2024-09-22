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

    # Serialize an object to a yaml file with optional extra `serde`
    temp_fs.ser("file2.yaml", {"key": "value"})

    # Serialize an object to a yaml file, with different options
    temp_fs.set_serde_kwargs(".yaml", indent=4)
    temp_fs.ser("file2.yaml", {"key": "value"})

    # Serialize a pydantic model with optional extra `pydantic`
    from pydantic import BaseModel

    class A(BaseModel):
        b: int
        c: str

    example = A(b=1, c="test")
    result = temp_fs.ser("a.json", example)

    # Create multiple files at once, even in sub directories.
    temp_fs.gen({"subdir": {"file1": "hello world", "file2": 42}})
```
