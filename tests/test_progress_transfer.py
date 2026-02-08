"""Integration tests for export/import progress use-cases."""

from __future__ import annotations

from datetime import datetime, timedelta

from python_learning_orchestrated.adapters.in_memory_practice_repository import (
    InMemoryPracticeRepository,
)
from python_learning_orchestrated.application.progress_transfer import (
    ExportProgress,
    ImportProgress,
)
from python_learning_orchestrated.domain.practice import Attempt, LearningItem


def test_export_import_round_trip_with_in_memory_repository() -> None:
    now = datetime(2025, 1, 1, 9, 0, 0)
    source = InMemoryPracticeRepository(
        [
            LearningItem(
                id="variables-review",
                prompt="What is a variable?",
                status="review",
                order=1,
                due_at=now + timedelta(days=1),
                review_level=1,
                interval_minutes=1440,
            ),
            LearningItem(
                id="loops-review",
                prompt="When to use for loops?",
                status="new",
                order=2,
            ),
        ]
    )
    source.record_attempt(
        Attempt(
            item_id="variables-review",
            timestamp=now,
            outcome="correct",
        )
    )

    snapshot = ExportProgress(source, now_provider=lambda: now).run()

    target = InMemoryPracticeRepository([])
    imported_snapshot = ImportProgress(target).run(snapshot)

    assert imported_snapshot.items == snapshot.items
    assert imported_snapshot.attempts == snapshot.attempts
    assert sorted(target.list_items(), key=lambda item: item.id) == sorted(
        source.list_items(), key=lambda item: item.id
    )
    assert target.list_attempts() == source.list_attempts()
