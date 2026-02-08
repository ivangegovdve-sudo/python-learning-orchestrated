"""Progress repository port definition."""

from __future__ import annotations

from abc import ABC, abstractmethod

from python_learning_orchestrated.domain.progress import LessonProgress


class ProgressRepository(ABC):
    """Persistence boundary for learner progress."""

    @abstractmethod
    def get_progress(self, user_id: str) -> LessonProgress:
        """Return a user's progress payload."""

    @abstractmethod
    def save_progress(self, user_id: str, progress: LessonProgress) -> None:
        """Persist a user's progress payload."""
