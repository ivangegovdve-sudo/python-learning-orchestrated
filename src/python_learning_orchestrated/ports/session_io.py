"""IO port for running interactive practice sessions."""

from __future__ import annotations

from abc import ABC, abstractmethod

from python_learning_orchestrated.domain.practice import LearningItem


class SessionIO(ABC):
    """Boundary for user-facing input and output in session flows."""

    @abstractmethod
    def write_line(self, line: str) -> None:
        """Display a line of text to the learner."""

    @abstractmethod
    def read_outcome(self, item: LearningItem) -> str:
        """Read user response for a prompted learning item."""
