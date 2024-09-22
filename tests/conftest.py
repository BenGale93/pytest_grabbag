import pytest

pytest_plugins = ["pytester"]


@pytest.fixture
def func_name(request: pytest.FixtureRequest):
    return request.node.name
