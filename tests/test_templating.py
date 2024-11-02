import pytest

from pytest_grabbag import exceptions
from pytest_grabbag.templating import TemplateManager


def test_gathered_simple_template(templates: TemplateManager):
    assert "simple" in templates.templates


def test_render_simple_template(templates: TemplateManager, named_temp_fs):
    templates.render("simple", named_temp_fs, project_name="test_project", module_name="test_module")

    test_module = named_temp_fs / "test_project" / "test_module.py"

    assert test_module.exists()
    assert test_module.read_text() == 'print("Hello from test_module!")'


def test_render_unknown_template(templates: TemplateManager, named_temp_fs):
    with pytest.raises(exceptions.UnknownTemplateError, match="fake"):
        templates.render("fake", named_temp_fs, project_name="test_project", module_name="test_module")
