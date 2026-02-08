"""In-memory progress repository adapter."""

from __future__ import annotations

from python_learning_orchestrated.domain.progress import LessonProgress
from python_learning_orchestrated.ports.progress_repository import ProgressRepository


class InMemoryProgressRepository(ProgressRepository):
    """Store progress payloads in local process memory."""

    def __init__(self) -> None:
        self._storage: dict[str, LessonProgress] = {}

    def get_progress(self, user_id: str) -> LessonProgress:
        """Return a copy of the stored progress for user_id."""
        return self._storage.get(user_id, {}).copy()

    def save_progress(self, user_id: str, progress: LessonProgress) -> None:
        """Save a copy of progress for user_id."""
        self._storage[user_id] = progress.copy()
