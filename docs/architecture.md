# Architecture (Phase 1)

## Folder structure

- `src/python_learning_orchestrated/`: application package and CLI entrypoint.
- `tests/`: automated tests (smoke tests for now).
- `.github/workflows/`: CI workflows.
- `docs/`: architecture and planning notes.

## Boundaries

- Keep business logic in package modules under `src/`.
- Keep CLI thin and delegate behavior to importable functions.
- Keep tests focused on public interfaces first.

## No magic principle

- Prefer explicit functions and straightforward control flow.
- Use predictable tooling (ruff, black, mypy, pytest) to enforce consistency.

## Future phases

- Add learning-domain entities and orchestration flows.
- Add data persistence and progress modeling.
- Expand CLI commands and package distribution options.
