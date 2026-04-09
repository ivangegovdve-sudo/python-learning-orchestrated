"""Tests for JSON file progress snapshot store adapter."""

from __future__ import annotations

import pytest

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


def test_load_payload_not_a_file(tmp_path) -> None:
    store = JsonFileProgressSnapshotStore(tmp_path)
    # create a directory
    store._file_path.mkdir(exist_ok=True)

    assert store._load_payload() == {}


def test_load_payload_exceeds_size_limit(tmp_path) -> None:
    file_path = tmp_path / "large_file.json"
    store = JsonFileProgressSnapshotStore(file_path)

    # write more than 10MB
    with open(file_path, "wb") as f:
        f.seek(10 * 1024 * 1024 + 5)
        f.write(b"\0")

    with pytest.raises(ValueError, match="exceeds 10MB size limit"):
        store._load_payload()
