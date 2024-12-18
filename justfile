default: lint type_check test

alias t := test

@test:
    COV_CORE_SOURCE=src COV_CORE_CONFIG=pyproject.toml COV_CORE_DATAFILE=.coverage.eager uv run --all-extras --group dev pytest
    uv run --group dev --all-extras coverage report --fail-under=100

alias tc := type_check

@type_check:
    uv run --group dev --all-extras mypy src/ tests/

alias l := lint

@lint:
    uv run --group dev ruff format .
    uv run --group dev ruff check . --fix
