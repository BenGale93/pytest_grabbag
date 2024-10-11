"""Grab bag of tools for dealing with temporary files and directories."""

import os
import typing as t
from contextlib import contextmanager
from pathlib import Path

from pytest import TempPathFactory, fixture  # noqa: PT013

from pytest_grabbag._serde import SerializationManager

PathLike = Path | str

AnyDict = dict[str, t.Any]


class TempFs(Path):
    """A subclass of Path that makes it easier to generate files and folders for testing."""

    def __init__(self, *args: str | os.PathLike[str]) -> None:
        """Initialise TempFs instance."""
        super().__init__(*args)
        self._serde_manager = SerializationManager()

    def set_serde_kwargs(self, extension: str, **kwargs: t.Any) -> None:
        """Set the keyword arguments for a serializer.

        You can use this to influence how the output is formatted, for example.
        """
        self._serde_manager.set_kwargs(extension, **kwargs)

    def write(self, file_name: PathLike, content: str | bytes = "") -> t.Self:
        """Write a file to the temporary file system.

        Args:
            file_name: The name of the file to write. Creates any parent directories required.
            content: The content to write to the file.

        Returns:
            The path to the file that was written.
        """
        new_file = self / file_name
        return self._write(new_file, content)

    def ser(self, file_name: PathLike, content: t.Any) -> t.Self:
        """Serialize content to a given file based of the type of file.

        Supported formats are:
            * yaml (".yml", ".yaml")
            * toml (".toml")
            * json (".json")
            * pickle (".pkl", ".pickle")

        Args:
            file_name: Name of the file to serialize to, must have a suffix.
            content: Content to serialize.

        Raises:
            UnsupportedSerializationError: If the file suffix is not supported.

        Returns:
            The file that was written to.
        """
        stringy_content = None
        new_file = Path(file_name)
        serializer = self._serde_manager.get_serializer(new_file.suffix)
        stringy_content = serializer(content)
        return self.write(file_name, stringy_content)

    def gen(self, structure: AnyDict, prefix: t.Self | None = None) -> list[t.Self]:
        """Generate a structure of files and directories.

        Structure of the file system is defined using dictionaries. The keys
        are the names of the folders/files and the values are either
        dictionaries, which represent subfolders, or the content of files.
        If the key is a file with a supported extension, the value will not
        be interpreted as a subfolder, rather an object to serialize.

        Args:
            structure: The file system structure and contents.
            prefix: Root of the generated file structure. Defaults to None, which then uses self.

        Returns:
            List of the Paths that were generated.
        """
        paths = []
        for name, content in structure.items():
            path = (prefix or self) / name
            if path.suffix and not isinstance(content, str):
                self.ser(path, content)
            elif isinstance(content, dict):
                if not content:
                    path.mkdir(parents=True, exist_ok=True)
                else:
                    self.gen(content, prefix=path)
            else:
                path = self._write(path, content)
            paths.append(path)
        return paths

    @contextmanager
    def chdir(self) -> t.Generator[None, None, None]:
        """Context manager for changing the working directory to the given folder."""
        current_working_dir = Path.cwd()
        try:
            os.chdir(self)
            yield None
        finally:
            os.chdir(current_working_dir)

    def _write(self, file_name: t.Self, content: str | bytes) -> t.Self:
        file_name.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            file_name.write_bytes(content)
        else:
            file_name.write_text(content, encoding="utf-8")
        return file_name


class TempFsFactory:
    """Factory for creating TempFs instances that represent a temporary file system."""

    def __init__(self, factory: TempPathFactory) -> None:
        """Initialise the factory with the pytest TempPathFactory to use."""
        self.factory = factory

    def mktemp(self, basename: str) -> TempFs:
        """Makes a temporary root folder with a given name."""
        return TempFs(self.factory.mktemp(basename))


@fixture(scope="session")
def temp_fs_factory(tmp_path_factory: TempPathFactory) -> TempFsFactory:
    """Fixture for creating temporary file systems.

    Wraps the pytest fixture `tmp_path_factory`.
    """
    return TempFsFactory(tmp_path_factory)
