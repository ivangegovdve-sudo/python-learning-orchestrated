"""Unit tests for domain merge semantics of progress snapshots."""

from __future__ import annotations

from datetime import datetime, timedelta

from python_learning_orchestrated.domain.practice import Attempt, LearningItem
from python_learning_orchestrated.domain.practice_progress import (
    ProgressSnapshot,
    merge_progress,
)


def test_merge_progress_is_idempotent() -> None:
    now = datetime(2025, 1, 2, 12, 0, 0)
    current_items = [
        LearningItem(id="a", prompt="A", status="new", order=1),
    ]
    current_attempts = [
        Attempt(item_id="a", timestamp=now, outcome="correct"),
    ]
    imported = ProgressSnapshot(
        version=1,
        exported_at=now,
        items=[
            LearningItem(
                id="a",
                prompt="A",
                status="review",
                order=1,
                due_at=now + timedelta(days=1),
                review_level=1,
                interval_minutes=1440,
            )
        ],
        attempts=[
            Attempt(item_id="a", timestamp=now + timedelta(minutes=1), outcome="skip")
        ],
    )

    first_items, first_attempts = merge_progress(
        current_items, current_attempts, imported
    )
    second_items, second_attempts = merge_progress(
        first_items, first_attempts, imported
    )

    assert second_items == first_items
    assert second_attempts == first_attempts


def test_merge_progress_prefers_more_meaningful_item_progress_and_unions_attempts() -> (
    None
):
    now = datetime(2025, 1, 2, 12, 0, 0)
    current_items = [
        LearningItem(
            id="a",
            prompt="A-old",
            status="review",
            order=3,
            due_at=now + timedelta(hours=1),
            review_level=1,
            interval_minutes=60,
        )
    ]
    imported = ProgressSnapshot(
        version=1,
        exported_at=now,
        items=[
            LearningItem(
                id="a",
                prompt="A-new",
                status="review",
                order=1,
                due_at=now + timedelta(days=3),
                review_level=2,
                interval_minutes=4320,
            ),
            LearningItem(id="b", prompt="B", status="new", order=2),
        ],
        attempts=[
            Attempt(item_id="a", timestamp=now, outcome="correct"),
            Attempt(
                item_id="a", timestamp=now + timedelta(minutes=5), outcome="incorrect"
            ),
        ],
    )

    merged_items, merged_attempts = merge_progress(
        current_items=current_items,
        current_attempts=[Attempt(item_id="a", timestamp=now, outcome="correct")],
        imported=imported,
    )

    by_id = {item.id: item for item in merged_items}
    assert by_id["a"].review_level == 2
    assert by_id["a"].interval_minutes == 4320
    assert by_id["a"].due_at == now + timedelta(days=3)
    assert by_id["b"].status == "new"

    assert len(merged_attempts) == 2
    assert {(entry.item_id, entry.timestamp) for entry in merged_attempts} == {
        ("a", now),
        ("a", now + timedelta(minutes=5)),
    }
