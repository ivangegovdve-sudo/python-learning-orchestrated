# Python Learning Orchestrated

## Overview
A beginner Python learning app scaffold using architecture-first design (hexagonal/ports-and-adapters). CLI-based application that demonstrates user progress tracking for learning paths.

## Project Architecture
- **Language**: Python 3.12
- **Package Manager**: uv
- **Build System**: hatchling
- **Structure**: Hexagonal architecture (ports & adapters)
  - `src/python_learning_orchestrated/` - Main package
    - `domain/` - Domain models (learning_path)
    - `ports/` - Port interfaces (progress_repository)
    - `adapters/` - Adapter implementations (in_memory_progress_repository)
    - `application/` - Application services (progress_service)
    - `cli.py` - CLI entrypoint
  - `tests/` - Test suite (pytest)

## Running
- **CLI**: `uv run python-learning`
- **Tests**: `uv run pytest`
- **Lint**: `uv run ruff check .`
- **Format**: `uv run black .`
- **Type check**: `uv run mypy`

## Recent Changes
- 2026-02-08: Initial Replit setup, installed dependencies with uv, all 7 tests passing.
