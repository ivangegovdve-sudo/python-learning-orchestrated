"""JSON file-backed progress repository adapter."""

from __future__ import annotations

import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import cast

from python_learning_orchestrated.domain.progress import LessonProgress
from python_learning_orchestrated.ports.progress_repository import ProgressRepository


class JsonFileProgressRepository(ProgressRepository):
    """Persist progress payloads to a JSON file on disk."""

    def __init__(self, file_path: str | Path) -> None:
        self._file_path = Path(file_path)
        self._file_path.parent.mkdir(parents=True, exist_ok=True)

    def get_progress(self, user_id: str) -> LessonProgress:
        """Return stored progress for user_id, or empty progress."""
        storage = self._load_storage()
        progress = storage.get(user_id, {})
        return progress.copy() if isinstance(progress, dict) else {}

    def save_progress(self, user_id: str, progress: LessonProgress) -> None:
        """Persist progress for user_id using an atomic replace."""
        storage = self._load_storage()
        storage[user_id] = progress.copy()
        self._save_storage(storage)

    def reset_progress(self, user_id: str) -> None:
        """Delete persisted progress for user_id while keeping other users."""
        storage = self._load_storage()
        if user_id in storage:
            del storage[user_id]
            self._save_storage(storage)

    def _load_storage(self) -> dict[str, LessonProgress]:
        """Load all persisted progress payloads."""
        if not self._file_path.exists():
            return {}

        try:
            content = self._file_path.read_text(encoding="utf-8")
            if not content.strip():
                return {}

            data = json.loads(content)
            if not isinstance(data, dict):
                return {}

            normalized: dict[str, LessonProgress] = {}
            for user_id, progress in data.items():
                if isinstance(user_id, str) and isinstance(progress, dict):
                    normalized[user_id] = cast(LessonProgress, progress)
            return normalized
        except (json.JSONDecodeError, OSError):
            return {}

    def _save_storage(self, storage: dict[str, LessonProgress]) -> None:
        """Persist the full storage document to disk."""
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
