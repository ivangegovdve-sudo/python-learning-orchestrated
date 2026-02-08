"""Checkpoint metadata and file-based storage helpers."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
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

_CHECKPOINT_FILENAME_SUFFIX = ".checkpoint.json"


@dataclass(frozen=True)
class Checkpoint:
    """Lightweight metadata for a stored progress checkpoint."""

    name: str
    created_at: datetime
    description: str | None = None


@dataclass(frozen=True)
class CheckpointRecord:
    """Checkpoint metadata paired with an exported progress snapshot."""

    metadata: Checkpoint
    progress: ProgressSnapshot


class CheckpointStore:
    """Simple filesystem-backed checkpoint storage."""

    def __init__(self, directory: Path | None = None) -> None:
        self._directory = directory or default_checkpoint_directory()
        self._directory.mkdir(parents=True, exist_ok=True)

    def save_checkpoint(
        self,
        name: str,
        progress: ProgressSnapshot,
        *,
        description: str | None = None,
    ) -> Checkpoint:
        metadata = Checkpoint(
            name=name,
            created_at=progress.exported_at,
            description=description,
        )
        payload: dict[str, object] = {
            "name": metadata.name,
            "created_at": metadata.created_at.isoformat(),
            "description": metadata.description,
            "progress": _snapshot_to_dict(progress),
        }
        _write_json(self._path_for_name(name), payload)
        return metadata

    def load_checkpoint(self, name: str) -> CheckpointRecord:
        payload = _read_json(self._path_for_name(name))
        progress_payload = payload.get("progress")
        parsed_progress_payload = (
            progress_payload if isinstance(progress_payload, dict) else {}
        )
        metadata = Checkpoint(
            name=str(payload.get("name", name)),
            created_at=datetime.fromisoformat(str(payload.get("created_at"))),
            description=_optional_str(payload.get("description")),
        )
        return CheckpointRecord(
            metadata=metadata,
            progress=_snapshot_from_dict(parsed_progress_payload),
        )

    def list_checkpoints(self) -> list[Checkpoint]:
        checkpoints: list[Checkpoint] = []
        for file_path in sorted(
            self._directory.glob(f"*{_CHECKPOINT_FILENAME_SUFFIX}")
        ):
            payload = _read_json(file_path)
            checkpoints.append(
                Checkpoint(
                    name=str(payload.get("name", _name_from_path(file_path))),
                    created_at=datetime.fromisoformat(str(payload.get("created_at"))),
                    description=_optional_str(payload.get("description")),
                )
            )
        return checkpoints

    def delete_checkpoint(self, name: str) -> None:
        self._path_for_name(name).unlink(missing_ok=True)

    def _path_for_name(self, name: str) -> Path:
        return self._directory / f"{_slugify(name)}{_CHECKPOINT_FILENAME_SUFFIX}"


def default_checkpoint_directory() -> Path:
    """Return the deterministic user-visible checkpoint directory."""

    config_root = Path.home() / ".config"
    return config_root / "python-learning-orchestrated" / "checkpoints"


def _slugify(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip()).strip("-").lower()
    return normalized or "checkpoint"


def _name_from_path(path: Path) -> str:
    return path.name.removesuffix(_CHECKPOINT_FILENAME_SUFFIX)


def _optional_str(value: object) -> str | None:
    return value if isinstance(value, str) else None


def _snapshot_to_dict(snapshot: ProgressSnapshot) -> dict[str, object]:
    return {
        "version": snapshot.version,
        "exported_at": snapshot.exported_at.isoformat(),
        "items": [_item_to_dict(item) for item in snapshot.items],
        "attempts": [_attempt_to_dict(attempt) for attempt in snapshot.attempts],
    }


def _snapshot_from_dict(payload: dict[str, object]) -> ProgressSnapshot:
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


def _read_json(path: Path) -> dict[str, object]:
    parsed = json.loads(path.read_text(encoding="utf-8"))
    return parsed if isinstance(parsed, dict) else {}


def _write_json(path: Path, payload: dict[str, object]) -> None:
    temp_path: Path | None = None
    try:
        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f"{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temp_file:
            json.dump(payload, temp_file)
            temp_file.flush()
            os.fsync(temp_file.fileno())
            temp_path = Path(temp_file.name)
        os.replace(temp_path, path)
    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()
