"""Domain models for learning paths and lessons."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Lesson:
    """A single lesson in a learning path."""

    id: str
    title: str
    content: str


@dataclass(slots=True)
class LearningPath:
    """A learning path that owns an ordered list of lessons."""

    id: str
    title: str
    description: str
    lessons: list[Lesson] = field(default_factory=list)

    def add_lesson(self, lesson: Lesson) -> None:
        """Append a lesson to the learning path while preserving order."""
        self.lessons.append(lesson)
