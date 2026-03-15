"""Tests for JSON file progress snapshot store adapter."""

from __future__ import annotations

from python_learning_orchestrated.adapters.json_file_progress_snapshot_store import _to_int

def test_to_int_with_valid_int() -> None:
    assert _to_int(42, default=0) == 42

def test_to_int_with_valid_string() -> None:
    assert _to_int("42", default=0) == 42

def test_to_int_with_invalid_string_raises_value_error_returns_default() -> None:
    assert _to_int("not_an_int", default=10) == 10

def test_to_int_with_invalid_type_returns_default() -> None:
    assert _to_int(None, default=5) == 5
    assert _to_int(["42"], default=5) == 5
