"""JSON file-backed adapter for practice repository port."""

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
from python_learning_orchestrated.ports.practice_repository import PracticeRepository


class JsonFilePracticeRepository(PracticeRepository):
    """Persist practice items and attempts in a JSON document."""

    def __init__(self, file_path: str | Path, seed_items: list[LearningItem]) -> None:
        self._file_path = Path(file_path)
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self._file_path.exists():
            self._save_storage(
                {"items": [_item_to_dict(item) for item in seed_items], "attempts": []}
            )

    def list_items(self) -> list[LearningItem]:
        storage = self._load_storage()
        raw_items = storage.get("items", [])
        if not isinstance(raw_items, list):
            return []
        return [
            _item_from_dict(entry) for entry in raw_items if isinstance(entry, dict)
        ]

    def save_item(self, item: LearningItem) -> None:
        self.save_items([item])

    def save_items(self, items: list[LearningItem]) -> None:
        if not items:
            return

        storage = self._load_storage()
        raw_items = storage.get("items", [])
        if not isinstance(raw_items, list):
            raw_items = []
            storage["items"] = raw_items

        item_dict = {}
        for i, entry in enumerate(raw_items):
            if isinstance(entry, dict):
                item_dict[str(entry.get("id"))] = i

        for item in items:
            item_id_str = str(item.id)
            if item_id_str in item_dict:
                raw_items[item_dict[item_id_str]] = _item_to_dict(item)
            else:
                raw_items.append(_item_to_dict(item))
                item_dict[item_id_str] = len(raw_items) - 1

        self._save_storage(storage)

    def list_attempts(self) -> list[Attempt]:
        storage = self._load_storage()
        raw_attempts = storage.get("attempts", [])
        if not isinstance(raw_attempts, list):
            return []
        attempts: list[Attempt] = []
        for entry in raw_attempts:
            if not isinstance(entry, dict):
                continue
            item_id = entry.get("item_id")
            timestamp = entry.get("timestamp")
            outcome = entry.get("outcome")
            if not isinstance(item_id, str) or not isinstance(timestamp, str):
                continue
            try:
                parsed_timestamp = datetime.fromisoformat(timestamp)
            except ValueError:
                continue
            normalized_outcome = (
                outcome if outcome in {"correct", "incorrect", "skip"} else "skip"
            )
            attempts.append(
                Attempt(
                    item_id=item_id,
                    timestamp=parsed_timestamp,
                    outcome=cast(AttemptOutcome, normalized_outcome),
                )
            )
        return attempts

    def record_attempt(self, attempt: Attempt) -> None:
        self.record_attempts([attempt])

    def record_attempts(self, attempts: list[Attempt]) -> None:
        if not attempts:
            return

        storage = self._load_storage()
        raw_attempts = storage.get("attempts", [])
        existing_attempts = raw_attempts if isinstance(raw_attempts, list) else []
        for attempt in attempts:
            existing_attempts.append(_attempt_to_dict(attempt))
        storage["attempts"] = existing_attempts
        self._save_storage(storage)

    def _load_storage(self) -> dict[str, object]:
        if not self._file_path.exists():
            return {"items": [], "attempts": []}
        if self._file_path.stat().st_size > 10 * 1024 * 1024:
            raise ValueError(
                f"Practice repository file {self._file_path} exceeds 10MB size limit"
            )

        try:
            content = self._file_path.read_text(encoding="utf-8")
            if not content.strip():
                return {"items": [], "attempts": []}
            parsed = json.loads(content)
            return parsed if isinstance(parsed, dict) else {"items": [], "attempts": []}
        except (OSError, json.JSONDecodeError):
            return {"items": [], "attempts": []}

    def _save_storage(self, storage: dict[str, object]) -> None:
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
                json.dump(storage, temp_file)
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
        "due_at": item.due_at.isoformat() if item.due_at is not None else None,
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


def _to_int(value: object, default: int) -> int:
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return default
    return default
