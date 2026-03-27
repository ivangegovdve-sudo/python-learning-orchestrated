from unittest.mock import MagicMock, patch

import pytest

from python_learning_orchestrated.adapters.checkpoint_store import CheckpointStore
from python_learning_orchestrated.adapters.json_file_practice_repository import (
    JsonFilePracticeRepository,
)


def test_practice_repo_ignores_non_regular_files(tmp_path):
    """Verify that device files like /dev/zero are ignored during read."""
    with patch("pathlib.Path.is_file", return_value=False):
        repo = JsonFilePracticeRepository(tmp_path / "repo.json", [])
        items = repo.list_items()
        assert items == []  # Empty when payload is {}


def test_checkpoint_store_enforces_bounded_read(tmp_path):
    """Verify that bounded read raises ValueError when file is too large."""
    with patch("pathlib.Path.is_file", return_value=True):
        mock_file = MagicMock()
        mock_file.__enter__.return_value.read.return_value = "x" * (
            10 * 1024 * 1024 + 2
        )

        with patch("builtins.open", return_value=mock_file):
            store = CheckpointStore(tmp_path)
            with pytest.raises(ValueError, match="exceeds 10MB size limit"):
                store.load_checkpoint("huge_checkpoint")
