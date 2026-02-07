"""Progress repository port definition."""

from __future__ import annotations

from abc import ABC, abstractmethod


class ProgressRepository(ABC):
    """Persistence boundary for learner progress."""

    @abstractmethod
    def get_progress(self, user_id: str) -> dict[str, object]:
        """Return a user's progress payload."""

    @abstractmethod
    def save_progress(self, user_id: str, progress: dict[str, object]) -> None:
        """Persist a user's progress payload."""
