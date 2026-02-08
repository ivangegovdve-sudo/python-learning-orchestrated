"""Unit tests for practice session domain policies."""

from __future__ import annotations

from datetime import datetime, timedelta

from python_learning_orchestrated.domain.practice import (
    LearningItem,
    select_next_item,
    update_schedule,
)

FIXED_NOW = datetime(2025, 1, 1, 9, 0, 0)


def test_select_next_item_prefers_earliest_due_review_then_stable_id() -> None:
    items = [
        LearningItem(
            id="review-b",
            prompt="B",
            status="review",
            order=99,
            due_at=FIXED_NOW - timedelta(minutes=5),
        ),
        LearningItem(
            id="review-a",
            prompt="A",
            status="review",
            order=99,
            due_at=FIXED_NOW - timedelta(minutes=5),
        ),
        LearningItem(id="new-1", prompt="N1", status="new", order=1),
    ]

    selected = select_next_item(items, FIXED_NOW)

    assert selected is not None
    assert selected.id == "review-a"


def test_select_next_item_falls_back_to_new_order_and_id() -> None:
    items = [
        LearningItem(id="new-2", prompt="N2", status="new", order=2),
        LearningItem(id="new-1-b", prompt="N1b", status="new", order=1),
        LearningItem(id="new-1-a", prompt="N1a", status="new", order=1),
    ]

    selected = select_next_item(items, FIXED_NOW)

    assert selected is not None
    assert selected.id == "new-1-a"


def test_update_schedule_correct_increases_interval_and_level() -> None:
    item = LearningItem(
        id="item-1", prompt="p", status="review", order=1, review_level=1
    )

    updated = update_schedule(item, "correct", FIXED_NOW)

    assert updated.review_level == 2
    assert updated.interval_minutes == 3 * 24 * 60
    assert updated.due_at == FIXED_NOW + timedelta(days=3)


def test_update_schedule_incorrect_resets_growth_and_schedules_soon() -> None:
    item = LearningItem(
        id="item-1",
        prompt="p",
        status="review",
        order=1,
        review_level=3,
        interval_minutes=7 * 24 * 60,
    )

    updated = update_schedule(item, "incorrect", FIXED_NOW)

    assert updated.review_level == 0
    assert updated.interval_minutes == 10
    assert updated.due_at == FIXED_NOW + timedelta(minutes=10)


def test_update_schedule_skip_does_not_change_item() -> None:
    item = LearningItem(
        id="item-1",
        prompt="p",
        status="review",
        order=1,
        due_at=FIXED_NOW,
        review_level=2,
        interval_minutes=100,
    )

    updated = update_schedule(item, "skip", FIXED_NOW)

    assert updated == item
