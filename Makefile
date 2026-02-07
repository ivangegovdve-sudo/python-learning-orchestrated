.PHONY: setup run test lint format typecheck ci

setup:
	uv sync --group dev
	uv run pre-commit install

run:
	uv run python-learning

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run black --check .

format:
	uv run ruff check --fix .
	uv run black .

typecheck:
	uv run mypy

ci: lint typecheck test
