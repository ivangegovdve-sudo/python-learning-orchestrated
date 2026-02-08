"""Unit tests for the in-memory progress repository."""

from __future__ import annotations

from python_learning_orchestrated.adapters.in_memory_progress_repository import (
    InMemoryProgressRepository,
)
from python_learning_orchestrated.domain.progress import LessonProgress


def test_save_and_get_progress_roundtrip() -> None:
    """Saved progress can be retrieved for the same user."""
    repository = InMemoryProgressRepository()
    progress: LessonProgress = {"lesson_id": "intro", "completed": True}

    repository.save_progress("user-123", progress)

    assert repository.get_progress("user-123") == progress
