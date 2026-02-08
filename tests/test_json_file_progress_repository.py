"""Unit tests for the JSON file progress repository."""

from __future__ import annotations

import json

from python_learning_orchestrated.adapters.json_file_progress_repository import (
    JsonFileProgressRepository,
)


def test_get_progress_missing_file_returns_empty(tmp_path) -> None:
    """Missing file should be treated as empty progress."""
    repository = JsonFileProgressRepository(tmp_path / "state" / "progress.json")

    assert repository.get_progress("user-123") == {}


def test_get_progress_invalid_json_returns_empty_and_recovers_on_save(tmp_path) -> None:
    """Invalid JSON should not crash and should be overwritten on next save."""
    progress_file = tmp_path / "progress.json"
    progress_file.write_text("{not-valid-json", encoding="utf-8")
    repository = JsonFileProgressRepository(progress_file)

    assert repository.get_progress("user-123") == {}

    repository.save_progress("user-123", {"lesson_id": "intro", "status": "completed"})

    data = json.loads(progress_file.read_text(encoding="utf-8"))
    assert data["user-123"]["lesson_id"] == "intro"


def test_save_and_get_progress_roundtrip(tmp_path) -> None:
    """Saved progress can be loaded by a new repository instance."""
    progress_file = tmp_path / "nested" / "progress.json"
    first = JsonFileProgressRepository(progress_file)

    first.save_progress("user-123", {"completed_lessons": ["variables"]})

    second = JsonFileProgressRepository(progress_file)
    assert second.get_progress("user-123") == {"completed_lessons": ["variables"]}


def test_atomic_save_results_in_valid_json_file(tmp_path) -> None:
    """Saving should leave a valid JSON file on disk."""
    progress_file = tmp_path / "progress.json"
    repository = JsonFileProgressRepository(progress_file)

    repository.save_progress(
        "user-1", {"lesson_id": "variables", "status": "completed"}
    )
    repository.save_progress(
        "user-2", {"lesson_id": "loops", "status": "completed"}
    )

    parsed = json.loads(progress_file.read_text(encoding="utf-8"))
    assert parsed["user-1"]["lesson_id"] == "variables"
    assert parsed["user-2"]["lesson_id"] == "loops"
