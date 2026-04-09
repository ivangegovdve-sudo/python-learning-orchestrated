import json
from pathlib import Path

from python_learning_orchestrated.adapters.json_file_practice_repository import (
    JsonFilePracticeRepository,
    _to_int,
)


def test_to_int_with_valid_string_returns_int():
    assert _to_int("123", 42) == 123


def test_to_int_with_invalid_string_returns_default():
    assert _to_int("abc", 42) == 42


def test_to_int_with_integer_returns_integer():
    assert _to_int(123, 42) == 123


def test_to_int_with_none_returns_default():
    assert _to_int(None, 42) == 42


def test_list_attempts_skips_invalid_timestamp(tmp_path: Path):
    file_path = tmp_path / "attempts.json"
    data = {
        "items": [],
        "attempts": [
            {
                "item_id": "item1",
                "timestamp": "2024-01-01T12:00:00Z",
                "outcome": "correct",
            },
            {
                "item_id": "item2",
                "timestamp": "invalid-timestamp",
                "outcome": "incorrect",
            },
        ],
    }
    file_path.write_text(json.dumps(data))

    repo = JsonFilePracticeRepository(file_path, seed_items=[])
    attempts = repo.list_attempts()

    assert len(attempts) == 1
    assert attempts[0].item_id == "item1"
    assert attempts[0].outcome == "correct"
