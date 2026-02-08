"""Checkpoint metadata and file-based storage helpers."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile

from python_learning_orchestrated.adapters.json_file_progress_snapshot_store import (
    progress_snapshot_from_payload,
    progress_snapshot_to_payload,
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
            "progress": progress_snapshot_to_payload(progress),
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
            progress=progress_snapshot_from_payload(parsed_progress_payload),
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
