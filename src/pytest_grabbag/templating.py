"""Module for templating test directories."""

import typing as t
from pathlib import Path

import pytest

from pytest_grabbag import _dependencies, exceptions, tmp_fs


class TemplateManager:
    """Class for managing copier templates used in testing."""

    def __init__(self, templates: dict[str, Path]) -> None:
        """Initialize a new template manager with the given templates."""
        self._templates = templates

    @property
    def templates(self) -> dict[str, Path]:
        """The dictionary of available templates."""
        return self._templates

    def render(self, template_name: str, target_dir: tmp_fs.TempFs, **template_data: t.Any) -> None:
        """Render the template with the given name in the target directory.

        Args:
            template_name: The folder name the template is located in.
            target_dir: The directory to render the template in.
            template_data: The data to pass to the template.
        """
        copier = _dependencies.import_optional("copier", "copier")
        try:
            template_path = self._templates[template_name]
        except KeyError:
            raise exceptions.UnknownTemplateError(template_name) from None
        copier.run_copy(str(template_path), target_dir, data=template_data)

    @classmethod
    def from_root(cls, search_path: Path) -> t.Self:
        """Create a TemplateManager by searching a root folder for copier.yml files.

        The name of the folder containing the copier.yml file will be used as the name of the template.
        """
        return cls(
            {template_yamls.parent.name: template_yamls.parent for template_yamls in search_path.rglob("copier.yml")}
        )


@pytest.fixture(scope="session")
def templates(request: pytest.FixtureRequest) -> TemplateManager:
    """Fixture that contains the available copier templates for the test suite."""
    _dependencies.import_optional("copier", "copier")
    return TemplateManager.from_root(request.config.rootpath / "tests")
