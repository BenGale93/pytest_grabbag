import pytest

from pytest_grabbag import exceptions
from pytest_grabbag.templating import TemplateManager
from pytest_grabbag.tmp_fs import TempFsFactory


def test_gathered_simple_template(templates: TemplateManager):
    assert "simple" in templates.templates


def test_render_simple_template(func_name, templates: TemplateManager, temp_fs_factory: TempFsFactory):
    tmp_fs = temp_fs_factory.mktemp(func_name)

    templates.render("simple", tmp_fs, project_name="test_project", module_name="test_module")

    test_module = tmp_fs / "test_project" / "test_module.py"

    assert test_module.exists()
    assert test_module.read_text() == 'print("Hello from test_module!")'


def test_render_unknown_template(func_name, templates: TemplateManager, temp_fs_factory: TempFsFactory):
    tmp_fs = temp_fs_factory.mktemp(func_name)
    with pytest.raises(exceptions.UnknownTemplateError, match="fake"):
        templates.render("fake", tmp_fs, project_name="test_project", module_name="test_module")
