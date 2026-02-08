"""Application service for practice session orchestration."""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime

from python_learning_orchestrated.domain.practice import (
    Attempt,
    AttemptOutcome,
    LearningItem,
    select_next_item,
    update_schedule,
)
from python_learning_orchestrated.ports.practice_repository import PracticeRepository
from python_learning_orchestrated.ports.session_io import SessionIO

NowProvider = Callable[[], datetime]


class RunPracticeSession:
    """Run the practice loop by coordinating domain policies and ports."""

    def __init__(
        self,
        repository: PracticeRepository,
        io: SessionIO,
        now_provider: NowProvider,
    ) -> None:
        self._repository = repository
        self._io = io
        self._now_provider = now_provider

    def run(self) -> None:
        """Execute practice rounds until user quits or no items are available."""
        self._io.write_line("Starting practice session.")

        while True:
            now = self._now_provider()
            next_item = select_next_item(self._repository.list_items(), now)
            if next_item is None:
                self._io.write_line(
                    "No due review or new items available. Session complete."
                )
                return

            self._io.write_line(f"Activity {next_item.id}: {next_item.prompt}")
            outcome = self._read_valid_outcome(next_item)
            if outcome is None:
                self._io.write_line("Session ended by user.")
                return

            self._repository.record_attempt(
                Attempt(item_id=next_item.id, timestamp=now, outcome=outcome)
            )

            updated_item = update_schedule(next_item, outcome, now)
            if updated_item != next_item:
                self._repository.save_item(updated_item)

            self._io.write_line(f"Recorded: {outcome} for {next_item.id}.")

    def _read_valid_outcome(self, item: LearningItem) -> AttemptOutcome | None:
        while True:
            normalized = self._io.read_outcome(item).strip().lower()
            if normalized in {"quit", "q"}:
                return None
            if normalized in {"correct", "c"}:
                return "correct"
            if normalized in {"incorrect", "i"}:
                return "incorrect"
            if normalized in {"skip", "s"}:
                return "skip"
            self._io.write_line(
                "Invalid response. Use: correct/c, incorrect/i, skip/s, or quit/q."
            )
