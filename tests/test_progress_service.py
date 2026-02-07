"""Unit tests for the progress application service."""

from __future__ import annotations

from python_learning_orchestrated.adapters.in_memory_progress_repository import (
    InMemoryProgressRepository,
)
from python_learning_orchestrated.application.progress_service import ProgressService


def test_record_user_progress_delegates_to_repository() -> None:
    """record_user_progress writes payload to injected repository."""
    repository = InMemoryProgressRepository()
    service = ProgressService(repository)
    progress = {"lesson_id": "variables", "completed": True}

    service.record_user_progress("user-123", progress)

    assert repository.get_progress("user-123") == progress


def test_get_user_progress_delegates_to_repository() -> None:
    """get_user_progress returns payload from injected repository."""
    repository = InMemoryProgressRepository()
    repository.save_progress("user-456", {"lesson_id": "loops", "completed": False})
    service = ProgressService(repository)

    assert service.get_user_progress("user-456") == {
        "lesson_id": "loops",
        "completed": False,
    }
