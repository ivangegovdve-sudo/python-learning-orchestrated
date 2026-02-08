"""Happy-path tests for checkpoint storage helpers."""

from __future__ import annotations

from datetime import datetime

from python_learning_orchestrated.adapters.checkpoint_store import CheckpointStore
from python_learning_orchestrated.domain.practice import Attempt, LearningItem
from python_learning_orchestrated.domain.practice_progress import ProgressSnapshot


def test_save_and_load_checkpoint_round_trip(tmp_path) -> None:
    store = CheckpointStore(tmp_path)
    snapshot = ProgressSnapshot(
        version=1,
        exported_at=datetime(2025, 1, 1, 9, 0, 0),
        items=[
            LearningItem(
                id="variables-review",
                prompt="What is a variable?",
                status="review",
                order=1,
            )
        ],
        attempts=[
            Attempt(
                item_id="variables-review",
                timestamp=datetime(2025, 1, 1, 9, 5, 0),
                outcome="correct",
            )
        ],
    )

    metadata = store.save_checkpoint("Week 1", snapshot, description="Before quiz")
    loaded = store.load_checkpoint("Week 1")

    assert metadata.name == "Week 1"
    assert metadata.created_at == snapshot.exported_at
    assert loaded.metadata == metadata
    assert loaded.progress == snapshot


def test_list_and_delete_checkpoints(tmp_path) -> None:
    store = CheckpointStore(tmp_path)
    first = ProgressSnapshot(
        version=1,
        exported_at=datetime(2025, 1, 1, 8, 0, 0),
        items=[],
        attempts=[],
    )
    second = ProgressSnapshot(
        version=1,
        exported_at=datetime(2025, 1, 2, 8, 0, 0),
        items=[],
        attempts=[],
    )

    store.save_checkpoint("Week 1", first)
    store.save_checkpoint("Week 2", second, description="After loops")

    checkpoints = store.list_checkpoints()

    assert [checkpoint.name for checkpoint in checkpoints] == ["Week 1", "Week 2"]
    assert checkpoints[1].description == "After loops"

    store.delete_checkpoint("Week 1")

    remaining = store.list_checkpoints()
    assert [checkpoint.name for checkpoint in remaining] == ["Week 2"]
