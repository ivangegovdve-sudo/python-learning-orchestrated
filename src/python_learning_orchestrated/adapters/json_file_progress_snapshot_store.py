"""JSON file adapter for import/export progress snapshots."""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import cast

from python_learning_orchestrated.domain.practice import (
    Attempt,
    AttemptOutcome,
    LearningItem,
)
from python_learning_orchestrated.domain.practice_progress import ProgressSnapshot
from python_learning_orchestrated.ports.progress_snapshot_store import (
    ProgressSnapshotStore,
)


class JsonFileProgressSnapshotStore(ProgressSnapshotStore):
    """Read and write progress snapshots at a JSON file path."""

    def __init__(self, file_path: str | Path) -> None:
        self._file_path = Path(file_path)
        self._file_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> ProgressSnapshot:
        return progress_snapshot_from_payload(self._load_payload())

    def save(self, snapshot: ProgressSnapshot) -> None:
        self._save_payload(progress_snapshot_to_payload(snapshot))

    def _load_payload(self) -> dict[str, object]:
        if not self._file_path.exists():
            return {}
        try:
            parsed = json.loads(self._file_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}
        return parsed if isinstance(parsed, dict) else {}

    def _save_payload(self, payload: dict[str, object]) -> None:
        temp_path: Path | None = None
        try:
            with NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self._file_path.parent,
                prefix=f"{self._file_path.name}.",
                suffix=".tmp",
                delete=False,
            ) as temp_file:
                json.dump(payload, temp_file)
                temp_file.flush()
                os.fsync(temp_file.fileno())
                temp_path = Path(temp_file.name)
            os.replace(temp_path, self._file_path)
        finally:
            if temp_path is not None and temp_path.exists():
                temp_path.unlink()


def _item_to_dict(item: LearningItem) -> dict[str, object]:
    return {
        "id": item.id,
        "prompt": item.prompt,
        "status": item.status,
        "order": item.order,
        "due_at": item.due_at.isoformat() if item.due_at else None,
        "review_level": item.review_level,
        "interval_minutes": item.interval_minutes,
    }


def progress_snapshot_to_payload(snapshot: ProgressSnapshot) -> dict[str, object]:
    """Serialize progress snapshot to the stable JSON payload shape."""

    return {
        "version": snapshot.version,
        "exported_at": snapshot.exported_at.isoformat(),
        "items": [_item_to_dict(item) for item in snapshot.items],
        "attempts": [_attempt_to_dict(attempt) for attempt in snapshot.attempts],
    }


def progress_snapshot_from_payload(payload: dict[str, object]) -> ProgressSnapshot:
    """Deserialize progress snapshot from the stable JSON payload shape."""

    raw_items = payload.get("items", [])
    raw_attempts = payload.get("attempts", [])

    item_entries = raw_items if isinstance(raw_items, list) else []
    attempt_entries = raw_attempts if isinstance(raw_attempts, list) else []

    items = [
        _item_from_dict(entry) for entry in item_entries if isinstance(entry, dict)
    ]
    attempts = [
        _attempt_from_dict(entry)
        for entry in attempt_entries
        if isinstance(entry, dict) and _has_attempt_required_fields(entry)
    ]

    exported_at_raw = payload.get("exported_at")
    exported_at = (
        datetime.fromisoformat(exported_at_raw)
        if isinstance(exported_at_raw, str)
        else datetime.fromtimestamp(0)
    )

    return ProgressSnapshot(
        version=_to_int(payload.get("version"), 1),
        exported_at=exported_at,
        items=items,
        attempts=attempts,
    )


def _item_from_dict(payload: dict[str, object]) -> LearningItem:
    due_at_raw = payload.get("due_at")
    due_at = datetime.fromisoformat(due_at_raw) if isinstance(due_at_raw, str) else None
    return LearningItem(
        id=str(payload.get("id", "")),
        prompt=str(payload.get("prompt", "")),
        status="review" if payload.get("status") == "review" else "new",
        order=_to_int(payload.get("order"), 0),
        due_at=due_at,
        review_level=_to_int(payload.get("review_level"), 0),
        interval_minutes=_to_int(payload.get("interval_minutes"), 0),
    )


def _attempt_to_dict(attempt: Attempt) -> dict[str, str]:
    return {
        "item_id": attempt.item_id,
        "timestamp": attempt.timestamp.isoformat(),
        "outcome": attempt.outcome,
    }


def _attempt_from_dict(payload: dict[str, object]) -> Attempt:
    outcome = str(payload.get("outcome", "skip"))
    normalized = outcome if outcome in {"correct", "incorrect", "skip"} else "skip"
    return Attempt(
        item_id=str(payload.get("item_id", "")),
        timestamp=datetime.fromisoformat(str(payload.get("timestamp"))),
        outcome=cast(AttemptOutcome, normalized),
    )


def _has_attempt_required_fields(payload: dict[str, object]) -> bool:
    return isinstance(payload.get("item_id"), str) and isinstance(
        payload.get("timestamp"), str
    )


def _to_int(value: object, default: int) -> int:
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return default
    return default
