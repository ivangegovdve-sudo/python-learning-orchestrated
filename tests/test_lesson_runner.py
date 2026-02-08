"""Unit tests for the lesson execution loop."""

from python_learning_orchestrated.adapters.in_memory_progress_repository import (
    InMemoryProgressRepository,
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


def test_run_next_lesson_completes_first_unfinished_lesson() -> None:
    repository = InMemoryProgressRepository()
    service = ProgressService(repository)
    runner = LessonRunner(service, _build_learning_path())

    result = runner.run_next_lesson("user-1")

    assert result == {"lesson_id": "lesson-1", "status": "completed"}
    assert service.get_user_progress("user-1") == {
        "lesson_id": "lesson-1",
        "status": "completed",
        "completed_lessons": ["lesson-1"],
    }


def test_run_next_lesson_skips_completed_lessons() -> None:
    repository = InMemoryProgressRepository()
    service = ProgressService(repository)
    service.record_user_progress(
        "user-2",
        {
            "lesson_id": "lesson-1",
            "status": "completed",
            "completed_lessons": ["lesson-1"],
        },
    )
    runner = LessonRunner(service, _build_learning_path())

    result = runner.run_next_lesson("user-2")

    assert result == {"lesson_id": "lesson-2", "status": "completed"}
    assert service.get_user_progress("user-2") == {
        "lesson_id": "lesson-2",
        "status": "completed",
        "completed_lessons": ["lesson-1", "lesson-2"],
    }


def test_run_next_lesson_reports_when_path_is_completed() -> None:
    repository = InMemoryProgressRepository()
    service = ProgressService(repository)
    service.record_user_progress(
        "user-3",
        {
            "lesson_id": "lesson-2",
            "status": "completed",
            "completed_lessons": ["lesson-1", "lesson-2"],
        },
    )
    runner = LessonRunner(service, _build_learning_path())

    result = runner.run_next_lesson("user-3")

    assert result == {"lesson_id": None, "status": "completed_all"}
