"""Tests for JSON file progress snapshot store adapter."""

from __future__ import annotations

from datetime import datetime

from python_learning_orchestrated.adapters.json_file_progress_snapshot_store import (
    _to_int,
    progress_snapshot_from_payload,
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


def test_progress_snapshot_from_payload_valid() -> None:
    payload: dict[str, object] = {
        "version": 2,
        "exported_at": "2023-10-27T10:00:00",
        "items": [
            {
                "id": "item1",
                "prompt": "prompt1",
                "status": "review",
                "order": 1,
                "due_at": "2023-10-28T10:00:00",
                "review_level": 2,
                "interval_minutes": 1440,
            }
        ],
        "attempts": [
            {
                "item_id": "item1",
                "timestamp": "2023-10-27T09:00:00",
                "outcome": "correct",
            }
        ],
    }

    snapshot = progress_snapshot_from_payload(payload)

    assert snapshot.version == 2
    assert snapshot.exported_at == datetime.fromisoformat("2023-10-27T10:00:00")

    assert len(snapshot.items) == 1
    assert snapshot.items[0].id == "item1"
    assert snapshot.items[0].prompt == "prompt1"
    assert snapshot.items[0].status == "review"
    assert snapshot.items[0].order == 1
    assert snapshot.items[0].due_at == datetime.fromisoformat("2023-10-28T10:00:00")
    assert snapshot.items[0].review_level == 2
    assert snapshot.items[0].interval_minutes == 1440

    assert len(snapshot.attempts) == 1
    assert snapshot.attempts[0].item_id == "item1"
    assert snapshot.attempts[0].timestamp == datetime.fromisoformat(
        "2023-10-27T09:00:00"
    )
    assert snapshot.attempts[0].outcome == "correct"


def test_progress_snapshot_from_payload_empty() -> None:
    snapshot = progress_snapshot_from_payload({})

    assert snapshot.version == 1
    assert snapshot.exported_at == datetime.fromtimestamp(0)
    assert snapshot.items == []
    assert snapshot.attempts == []


def test_progress_snapshot_from_payload_invalid_lists() -> None:
    payload: dict[str, object] = {
        "items": "not_a_list",
        "attempts": {"not": "a list"},
    }

    snapshot = progress_snapshot_from_payload(payload)

    assert snapshot.items == []
    assert snapshot.attempts == []


def test_progress_snapshot_from_payload_invalid_entries_in_list() -> None:
    payload: dict[str, object] = {
        "items": ["string_instead_of_dict", 42],
        "attempts": [None, 3.14],
    }

    snapshot = progress_snapshot_from_payload(payload)

    assert snapshot.items == []
    assert snapshot.attempts == []


def test_progress_snapshot_from_payload_invalid_attempt_fields() -> None:
    payload: dict[str, object] = {
        "attempts": [
            {"item_id": "item1"},  # missing timestamp
            {"timestamp": "2023-10-27T09:00:00"},  # missing item_id
            {
                "item_id": 123,
                "timestamp": "2023-10-27T09:00:00",
            },  # item_id not a string
            {
                "item_id": "item1",
                "timestamp": 1234567890,
            },  # timestamp not a string
            {"item_id": "item2", "timestamp": "2023-10-27T09:00:00"},  # valid
        ]
    }

    snapshot = progress_snapshot_from_payload(payload)

    assert len(snapshot.attempts) == 1
    assert snapshot.attempts[0].item_id == "item2"


def test_progress_snapshot_from_payload_invalid_exported_at() -> None:
    payload: dict[str, object] = {"exported_at": 1234567890}

    snapshot = progress_snapshot_from_payload(payload)

    assert snapshot.exported_at == datetime.fromtimestamp(0)
