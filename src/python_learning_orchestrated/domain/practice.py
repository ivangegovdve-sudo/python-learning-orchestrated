"""Domain models and policies for practice sessions."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timedelta
from typing import Literal

ItemStatus = Literal["new", "review"]
AttemptOutcome = Literal["correct", "incorrect", "skip"]


@dataclass(frozen=True, slots=True)
class LearningItem:
    """A practice activity with scheduling metadata."""

    id: str
    prompt: str
    status: ItemStatus
    order: int
    due_at: datetime | None = None
    review_level: int = 0
    interval_minutes: int = 0


@dataclass(frozen=True, slots=True)
class Attempt:
    """A learner attempt for a specific learning item."""

    item_id: str
    timestamp: datetime
    outcome: AttemptOutcome


def select_next_item(items: list[LearningItem], now: datetime) -> LearningItem | None:
    """Return the next item to practice using deterministic priority rules."""
    due_reviews = [
        item
        for item in items
        if item.status == "review" and item.due_at is not None and item.due_at <= now
    ]
    if due_reviews:
        return sorted(due_reviews, key=lambda item: (item.due_at, item.id))[0]

    new_items = [item for item in items if item.status == "new"]
    if new_items:
        return sorted(new_items, key=lambda item: (item.order, item.id))[0]

    return None


def update_schedule(
    item: LearningItem,
    outcome: AttemptOutcome,
    now: datetime,
) -> LearningItem:
    """Update scheduling metadata for an item after an attempt outcome."""
    if outcome == "skip":
        return item

    if outcome == "incorrect":
        return replace(
            item,
            status="review",
            due_at=now + timedelta(minutes=10),
            review_level=0,
            interval_minutes=10,
        )

    next_level = item.review_level + 1
    interval_minutes = _interval_minutes_for_level(next_level)
    return replace(
        item,
        status="review",
        due_at=now + timedelta(minutes=interval_minutes),
        review_level=next_level,
        interval_minutes=interval_minutes,
    )


def _interval_minutes_for_level(level: int) -> int:
    if level <= 1:
        return 24 * 60
    if level == 2:
        return 3 * 24 * 60
    if level == 3:
        return 7 * 24 * 60
    return int((7 * 24 * 60) * (2 ** (level - 3)))
