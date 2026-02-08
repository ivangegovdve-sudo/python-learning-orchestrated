"""Command-line entrypoint for the project."""

from __future__ import annotations

import argparse

from python_learning_orchestrated.adapters.in_memory_progress_repository import (
    InMemoryProgressRepository,
)
from python_learning_orchestrated.adapters.json_file_progress_repository import (
    JsonFileProgressRepository,
)
from python_learning_orchestrated.application.lesson_runner import LessonRunner
from python_learning_orchestrated.application.progress_service import ProgressService
from python_learning_orchestrated.domain.learning_path import LearningPath, Lesson
from python_learning_orchestrated.ports.progress_repository import ProgressRepository


def _build_parser() -> argparse.ArgumentParser:
    """Create CLI argument parser."""
    parser = argparse.ArgumentParser(description="Run python learning orchestrator")
    parser.add_argument(
        "--progress-file",
        type=str,
        default=None,
        help="Persist user progress in the given JSON file path.",
    )
    return parser


def _build_repository(progress_file: str | None) -> ProgressRepository:
    """Create repository adapter from CLI options."""
    if progress_file:
        return JsonFileProgressRepository(progress_file)
    return InMemoryProgressRepository()


def main(argv: list[str] | None = None) -> None:
    """Run a minimal CLI flow that executes the next lesson."""
    args = _build_parser().parse_args(argv)

    user_id = "demo-user"
    repository = _build_repository(args.progress_file)
    service = ProgressService(repository)
    learning_path = LearningPath(
        id="python-basics",
        title="Python Basics",
        description="A starter learning path for Python fundamentals.",
        lessons=[
            Lesson(
                id="variables",
                title="Variables",
                content="Learn how to declare and use variables.",
            ),
            Lesson(
                id="loops",
                title="Loops",
                content="Learn how to iterate with for and while loops.",
            ),
        ],
    )

    runner = LessonRunner(service, learning_path)
    result = runner.run_next_lesson(user_id)
    print(result)


if __name__ == "__main__":
    main()
