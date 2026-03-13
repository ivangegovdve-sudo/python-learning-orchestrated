"""Practice session repository port definition."""

from __future__ import annotations

from abc import ABC, abstractmethod

from python_learning_orchestrated.domain.practice import Attempt, LearningItem


class PracticeRepository(ABC):
    """Persistence boundary for practice scheduling and attempts."""

    @abstractmethod
    def list_items(self) -> list[LearningItem]:
        """Return all available learning items."""

    @abstractmethod
    def save_item(self, item: LearningItem) -> None:
        """Persist item scheduling state."""

    def save_items(self, items: list[LearningItem]) -> None:
        """Persist multiple items scheduling state."""
        for item in items:
            self.save_item(item)

    @abstractmethod
    def list_attempts(self) -> list[Attempt]:
        """Return all recorded attempts."""

    @abstractmethod
    def record_attempt(self, attempt: Attempt) -> None:
        """Persist an attempt record."""

    def record_attempts(self, attempts: list[Attempt]) -> None:
        """Persist multiple attempt records."""
        for attempt in attempts:
            self.record_attempt(attempt)
