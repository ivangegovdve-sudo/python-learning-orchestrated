# Python Learning Orchestrated

[![CI](https://github.com/<owner>/python-learning-orchestrated/actions/workflows/ci.yml/badge.svg)](https://github.com/<owner>/python-learning-orchestrated/actions/workflows/ci.yml)

Architecture-first beginner Python learning app.

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv)

## Setup

```bash
uv sync --group dev
uv run pre-commit install
```

## Run

```bash
uv run python-learning
```

Run the practice session orchestrator:

```bash
uv run python-learning session
```

## Test

```bash
uv run pytest
```

## Lint

```bash
uv run ruff check .
uv run ruff format --check .
```

## Typecheck

```bash
uv run mypy
```

## Roadmap (stub)

- [x] Phase 1: scaffold, quality gates, hello module, smoke tests.
- [ ] Phase 2: learning paths domain model.
- [ ] Phase 3: persistence and progress tracking.
- [ ] Phase 4: richer CLI/UX and packaging.
