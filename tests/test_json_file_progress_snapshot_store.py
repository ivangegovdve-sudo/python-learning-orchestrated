"""Tests for JSON file progress snapshot store adapter."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from python_learning_orchestrated.adapters.json_file_progress_snapshot_store import (
    JsonFileProgressSnapshotStore,
    _to_int,
)


def test_to_int_with_valid_int() -> None:
    assert _to_int(42, default=0) == 42


def test_to_int_with_valid_string() -> None:
    assert _to_int("42", default=0) == 42


def test_to_int_with_invalid_string_raises_value_error_returns_default() -> None:
    assert _to_int("not_an_int", default=10) == 10


def test_to_int_with_invalid_type_returns_default() -> None:
    assert _to_int(None, default=5) == 5
    assert _to_int(["42"], default=5) == 5


def test_load_payload_with_os_error(tmp_path: Path) -> None:
    file_path = tmp_path / "snapshot.json"
    file_path.write_text('{"version": 1}')

    store = JsonFileProgressSnapshotStore(file_path)

    with patch.object(Path, "read_text", side_effect=OSError("Mocked OSError")):
        snapshot = store.load()

    assert snapshot.version == 1
    assert snapshot.items == []
    assert snapshot.attempts == []


def test_load_payload_with_json_decode_error(tmp_path: Path) -> None:
    file_path = tmp_path / "snapshot.json"
    file_path.write_text("{invalid_json")

    store = JsonFileProgressSnapshotStore(file_path)
    snapshot = store.load()

    assert snapshot.version == 1
    assert snapshot.items == []
    assert snapshot.attempts == []
