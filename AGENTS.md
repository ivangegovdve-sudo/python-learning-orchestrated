# AGENTS.md - Python Learning Orchestrated Working Guide

This repository is an architecture-first beginner Python learning product. Treat it as a real learning system, not just a scaffold or notes dump.

## Goal

- build a structured beginner-friendly Python learning app
- keep the architecture understandable enough for learners and contributors
- turn the repo into a coherent product that can teach, assess, and track progress over time

## Current Idea And Progress

- Product idea:
  a guided Python learning experience with lessons, exercises, and clear progression
- Current state:
  scaffolded project with packaging, docs, tests, and CLI wiring in place
- Progress level:
  early foundation stage
- What is missing:
  substantial lesson content, learning flows, persistence, and polished UX

## Initial Setup Requirements

- Python `3.12+`
- `uv`
- recommended setup:
  `uv sync --group dev`
- install hooks:
  `uv run pre-commit install`
- run tests:
  `uv run pytest`
- run the app:
  `uv run python-learning`

## Environments

- local development:
  CLI-first Python environment
- CI:
  expected via GitHub Actions or equivalent Python checks
- staging / production:
  not yet defined

## Dependencies

- Python packaging from `pyproject.toml`
- dev tooling:
  `pytest`, `ruff`, `mypy`, `pre-commit`
- no mandatory external service dependencies today

## Backend Need

- backend required now:
  no
- backend recommended later:
  optional
- likely future backend:
  lightweight FastAPI service with SQLite or Postgres for user progress, synced lessons, analytics, and admin tools

## Backend Development Plan

1. Keep the first milestone backend-free and local-first.
2. Define the learning domain model:
   lessons, modules, exercises, attempts, hints, progress states.
3. Add local persistence first, either flat files or SQLite.
4. Introduce FastAPI only when multi-user sync, dashboards, or web delivery make it necessary.
5. Keep the teaching logic reusable so the same lesson engine can power CLI and web interfaces.

## How Development Should Progress

1. Finish the learning architecture before building a flashy UI.
2. Define the curriculum map:
   Python basics, control flow, functions, data structures, files, modules, debugging, testing.
3. Create real exercises with expected outputs and feedback loops.
4. Add progress tracking and learner checkpoints.
5. Add instructor / parent / self-study reporting only after the core learner experience works.

## Product Roadmap

- Phase 1:
  solid CLI learning flows and real lesson content
- Phase 2:
  persistence, scoring, and progress summaries
- Phase 3:
  browser-based learner UI or teacher dashboard if needed
- Phase 4:
  richer assessments, adaptive guidance, and exported reports

## End Goal

The end goal is a genuinely useful beginner Python learning product that can start simple in the CLI, then grow into a structured educational system with progress tracking, assessments, and eventually a web interface if that helps the learning experience.
