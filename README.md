# Pytest Grab-Bag

A collection of miscellaneous pytest fixtures and plugins. Primarily aimed at
testing CLI apps. Most features that require dependencies are behind optional
extras so you can pick and choose what you need.

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

    # Change the working directory to the temporary file system.
    with temp_fs.chdir():
        pass
```

You can also immediately get a `TempFs` instance with the root name the same as
the test function.

```python
def test_creation_of_html(named_temp_fs):
    foo = Foo()

    with temp_fs.chdir():
        foo.to_html()
```

This is particularly useful if you want to visually inspect the output of a
test function. If you navigate to
`/tmp/pytest-of-$USER/pytest-$NUMBER/test_creation_of_html/` or equivalent, you
can see the actual HTML file that was generated.

## Copier templates

It can be useful to define folder structures using a copier template and then
run tests from within. Add the optional extra `copier` and you can easily
render these templates from within a test.

```python
def test_copier_stuff(templates, named_temp_fs):
    templates.render(
        "folder_template_is_in",
        named_temp_fs,
        project_name="test_project",
        module_name="test_module"
    )

    assert (named_temp_fs / "test_project").exists()
```
