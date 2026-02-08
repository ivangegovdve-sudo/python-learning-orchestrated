"""Application service for learner progress use cases."""

from __future__ import annotations

from python_learning_orchestrated.domain.progress import LessonProgress
from python_learning_orchestrated.ports.progress_repository import ProgressRepository


class ProgressService:
    """Coordinate progress-related use cases through a repository port."""

    def __init__(self, repository: ProgressRepository) -> None:
        self._repository = repository

    def get_user_progress(self, user_id: str) -> LessonProgress:
        """Return persisted progress for a user."""
        return self._repository.get_progress(user_id)

    def record_user_progress(self, user_id: str, progress: LessonProgress) -> None:
        """Persist progress data for a user."""
        self._repository.save_progress(user_id, progress)

    def reset_user_progress(self, user_id: str) -> None:
        """Clear persisted progress for a specific user."""
        self._repository.reset_progress(user_id)
