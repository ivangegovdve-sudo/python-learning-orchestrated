"""Use-cases for exporting and importing practice progress.

Stability Contract (frozen):
- Export returns a `ProgressSnapshot` containing repository items, repository
  attempts, the injected `now_provider()` timestamp, and the configured version.
- Import is additive and deterministic: it merges item progress by id, unions
  attempts by `(item_id, timestamp)`, writes only missing attempt keys, and
  returns a snapshot that preserves the imported `version` and `exported_at`.
- Running import with the same snapshot repeatedly is idempotent for resulting
  stored items and attempts.

Out of scope for this feature version:
- Snapshot/schema migration, compatibility across versions, or version
  negotiation.
- Conflict-resolution strategies beyond the existing domain merge semantics.
- Partial import/export, filtering, deletion, rollback, encryption, signing,
  transport/protocol concerns, or cross-repository transaction guarantees.
"""

from collections.abc import Callable
from datetime import datetime

from python_learning_orchestrated.domain.practice_progress import (
    ProgressSnapshot,
    merge_progress,
)
from python_learning_orchestrated.ports.practice_repository import PracticeRepository

NowProvider = Callable[[], datetime]


class ExportProgress:
    """Export repository progress as a domain snapshot."""

    def __init__(
        self,
        repository: PracticeRepository,
        now_provider: NowProvider,
        *,
        version: int = 1,
    ) -> None:
        self._repository = repository
        self._now_provider = now_provider
        self._version = version

    def run(self) -> ProgressSnapshot:
        return ProgressSnapshot(
            version=self._version,
            exported_at=self._now_provider(),
            items=self._repository.list_items(),
            attempts=self._repository.list_attempts(),
        )


class ImportProgress:
    """Import and merge a progress snapshot into repository state."""

    def __init__(self, repository: PracticeRepository) -> None:
        self._repository = repository

    def run(self, snapshot: ProgressSnapshot) -> ProgressSnapshot:
        current_items = self._repository.list_items()
        current_attempts = self._repository.list_attempts()

        merged_items, merged_attempts = merge_progress(
            current_items=current_items,
            current_attempts=current_attempts,
            imported=snapshot,
        )

        current_items_by_id = {item.id: item for item in current_items}
        changed_items = [
            item for item in merged_items if item != current_items_by_id.get(item.id)
        ]
        if changed_items:
            self._repository.save_items(changed_items)

        existing_attempt_keys = {
            (attempt.item_id, attempt.timestamp) for attempt in current_attempts
        }
        new_attempts = []
        for attempt in merged_attempts:
            key = (attempt.item_id, attempt.timestamp)
            if key not in existing_attempt_keys:
                new_attempts.append(attempt)
                existing_attempt_keys.add(key)

        if new_attempts:
            self._repository.record_attempts(new_attempts)

        return ProgressSnapshot(
            version=snapshot.version,
            exported_at=snapshot.exported_at,
            items=merged_items,
            attempts=merged_attempts,
        )
