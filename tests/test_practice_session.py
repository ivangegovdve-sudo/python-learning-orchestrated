"""Application integration tests for practice session use case."""

from __future__ import annotations

from collections import deque
from datetime import datetime, timedelta

from python_learning_orchestrated.adapters.in_memory_practice_repository import (
    InMemoryPracticeRepository,
)
from python_learning_orchestrated.application.practice_session import (
    RunPracticeSession,
)
from python_learning_orchestrated.domain.practice import LearningItem
from python_learning_orchestrated.ports.session_io import SessionIO


class FakeSessionIO(SessionIO):
    def __init__(self, responses: list[str]) -> None:
        self._responses = deque(responses)
        self.lines: list[str] = []

    def write_line(self, line: str) -> None:
        self.lines.append(line)

    def read_outcome(self, item: LearningItem) -> str:
        return self._responses.popleft()


def test_run_practice_session_prefers_due_then_new_and_persists_attempts() -> None:
    fixed_now = datetime(2025, 1, 1, 12, 0, 0)
    now_values = deque(
        [
            fixed_now,
            fixed_now + timedelta(minutes=1),
            fixed_now + timedelta(minutes=2),
        ]
    )

    repository = InMemoryPracticeRepository(
        [
            LearningItem(
                id="review-1",
                prompt="due review",
                status="review",
                order=50,
                due_at=fixed_now - timedelta(minutes=30),
                review_level=1,
            ),
            LearningItem(
                id="new-1",
                prompt="first new",
                status="new",
                order=1,
            ),
        ]
    )
    io = FakeSessionIO(["correct", "skip", "quit"])

    session = RunPracticeSession(
        repository=repository,
        io=io,
        now_provider=lambda: now_values[0]
        if len(now_values) == 1
        else now_values.popleft(),
    )

    session.run()

    attempts = repository.list_attempts()
    assert [attempt.item_id for attempt in attempts] == ["review-1", "new-1"]
    assert [attempt.outcome for attempt in attempts] == ["correct", "skip"]

    items_by_id = {item.id: item for item in repository.list_items()}
    assert items_by_id["review-1"].review_level == 2
    assert items_by_id["review-1"].due_at == fixed_now + timedelta(days=3)
    assert items_by_id["new-1"].status == "new"
    assert "Activity review-1: due review" in io.lines
    assert "Activity new-1: first new" in io.lines
