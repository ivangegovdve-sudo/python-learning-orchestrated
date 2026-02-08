"""Unit tests for text-based interactive UI actions."""

from __future__ import annotations

from python_learning_orchestrated.adapters.in_memory_progress_repository import (
    InMemoryProgressRepository,
)
from python_learning_orchestrated.application.interactive_ui import (
    InteractiveLearningUI,
    progress_summary,
    reset_progress,
    show_progress,
    start_or_continue_learning,
)
from python_learning_orchestrated.application.lesson_runner import LessonRunner
from python_learning_orchestrated.application.progress_service import ProgressService
from python_learning_orchestrated.domain.learning_path import LearningPath, Lesson


def _build_learning_path() -> LearningPath:
    return LearningPath(
        id="lp-python-basics",
        title="Python Basics",
        description="A starter learning path for Python fundamentals.",
        lessons=[
            Lesson(id="lesson-1", title="Variables", content="Variables lesson"),
            Lesson(id="lesson-2", title="Loops", content="Loops lesson"),
        ],
    )


def test_start_or_continue_learning_completes_next_lesson() -> None:
    repository = InMemoryProgressRepository()
    service = ProgressService(repository)
    learning_path = _build_learning_path()
    runner = LessonRunner(service, learning_path)

    result = start_or_continue_learning(runner, service, learning_path, "user-1")

    assert result.should_exit is False
    assert result.lines[0] == "Completed lesson: lesson-1"


def test_show_progress_lists_completed_and_pending_lessons() -> None:
    repository = InMemoryProgressRepository()
    service = ProgressService(repository)
    learning_path = _build_learning_path()
    service.record_user_progress(
        "user-2",
        {
            "lesson_id": "lesson-1",
            "status": "completed",
            "completed_lessons": ["lesson-1"],
        },
    )

    result = show_progress(service, learning_path, "user-2")

    assert result.lines == [
        "Progress by lesson:",
        "- lesson-1: completed",
        "- lesson-2: pending",
    ]


def test_reset_progress_clears_only_current_user() -> None:
    repository = InMemoryProgressRepository()
    service = ProgressService(repository)
    service.record_user_progress("user-1", {"completed_lessons": ["lesson-1"]})
    service.record_user_progress("user-2", {"completed_lessons": ["lesson-2"]})

    result = reset_progress(service, "user-1")

    assert result.lines == ["Progress reset for user: user-1"]
    assert service.get_user_progress("user-1") == {}
    assert service.get_user_progress("user-2") == {"completed_lessons": ["lesson-2"]}


def test_progress_summary_returns_completed_and_total() -> None:
    repository = InMemoryProgressRepository()
    service = ProgressService(repository)
    learning_path = _build_learning_path()
    service.record_user_progress("user-1", {"completed_lessons": ["lesson-1"]})

    assert progress_summary(service, learning_path, "user-1") == (1, 2)


def test_handle_menu_choice_returns_exit_on_zero() -> None:
    repository = InMemoryProgressRepository()
    service = ProgressService(repository)
    learning_path = _build_learning_path()
    runner = LessonRunner(service, learning_path)
    ui = InteractiveLearningUI("demo-user", service, runner, learning_path)

    result = ui.handle_menu_choice("0")

    assert result.should_exit is True
    assert result.lines == ["Goodbye!"]
