"""Domain progress value types."""

from __future__ import annotations

from typing import TypedDict


class LessonProgress(TypedDict, total=False):
    """Persisted learner progress payload."""

    lesson_id: str
    status: str
    completed_lessons: list[str]
    completed: bool
