"""Domain DTOs and merge rules for progress import/export."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from python_learning_orchestrated.domain.practice import Attempt, LearningItem


@dataclass(frozen=True, slots=True)
class ProgressSnapshot:
    """Serializable progress state for learning items and attempts."""

    version: int
    exported_at: datetime
    items: list[LearningItem]
    attempts: list[Attempt]


def merge_progress(
    current_items: list[LearningItem],
    current_attempts: list[Attempt],
    imported: ProgressSnapshot,
) -> tuple[list[LearningItem], list[Attempt]]:
    """Merge imported snapshot data into current progress state."""
    merged_items = _merge_items(current_items, imported.items)
    merged_attempts = _merge_attempts(current_attempts, imported.attempts)
    return merged_items, merged_attempts


def _merge_items(
    current_items: list[LearningItem], imported_items: list[LearningItem]
) -> list[LearningItem]:
    by_id = {item.id: item for item in current_items}
    for imported_item in imported_items:
        existing = by_id.get(imported_item.id)
        if existing is None:
            by_id[imported_item.id] = imported_item
            continue
        by_id[imported_item.id] = _pick_more_progressed(existing, imported_item)
    return sorted(by_id.values(), key=lambda item: (item.order, item.id))


def _pick_more_progressed(first: LearningItem, second: LearningItem) -> LearningItem:
    first_score = _item_progress_score(first)
    second_score = _item_progress_score(second)
    if second_score > first_score:
        return second
    if first_score > second_score:
        return first
    if second.order < first.order:
        return second
    return first


def _item_progress_score(item: LearningItem) -> tuple[int, int, int, float]:
    due_ts = item.due_at.timestamp() if item.due_at is not None else float("-inf")
    return (
        1 if item.status == "review" else 0,
        item.review_level,
        item.interval_minutes,
        due_ts,
    )


def _merge_attempts(
    current_attempts: list[Attempt], imported_attempts: list[Attempt]
) -> list[Attempt]:
    deduped: dict[tuple[str, datetime], Attempt] = {
        (attempt.item_id, attempt.timestamp): attempt for attempt in current_attempts
    }
    for attempt in imported_attempts:
        deduped[(attempt.item_id, attempt.timestamp)] = attempt
    return sorted(
        deduped.values(), key=lambda attempt: (attempt.timestamp, attempt.item_id)
    )
