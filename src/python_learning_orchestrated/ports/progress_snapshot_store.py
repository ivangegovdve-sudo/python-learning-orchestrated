"""Port for reading/writing serialized progress snapshots."""

from __future__ import annotations

from abc import ABC, abstractmethod

from python_learning_orchestrated.domain.practice_progress import ProgressSnapshot


class ProgressSnapshotStore(ABC):
    """Boundary for snapshot serialization IO."""

    @abstractmethod
    def load(self) -> ProgressSnapshot:
        """Load a progress snapshot from storage."""

    @abstractmethod
    def save(self, snapshot: ProgressSnapshot) -> None:
        """Persist a progress snapshot to storage."""
