"""In-memory adapter for practice repository port."""

from __future__ import annotations

from python_learning_orchestrated.domain.practice import Attempt, LearningItem
from python_learning_orchestrated.ports.practice_repository import PracticeRepository


class InMemoryPracticeRepository(PracticeRepository):
    """Store practice items and attempts in process memory."""

    def __init__(self, items: list[LearningItem] | None = None) -> None:
        seed_items = items or []
        self._items: dict[str, LearningItem] = {item.id: item for item in seed_items}
        self._attempts: list[Attempt] = []

    def list_items(self) -> list[LearningItem]:
        return list(self._items.values())

    def save_item(self, item: LearningItem) -> None:
        self._items[item.id] = item

    def record_attempt(self, attempt: Attempt) -> None:
        self._attempts.append(attempt)

    def list_attempts(self) -> list[Attempt]:
        """Testing helper for verifying recorded attempts."""
        return [*self._attempts]
