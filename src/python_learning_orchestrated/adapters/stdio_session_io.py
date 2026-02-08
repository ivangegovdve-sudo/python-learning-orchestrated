"""Standard input/output adapter for practice sessions."""

from __future__ import annotations

from collections.abc import Callable

from python_learning_orchestrated.domain.practice import LearningItem
from python_learning_orchestrated.ports.session_io import SessionIO

InputFn = Callable[[], str]
OutputFn = Callable[[str], None]


class StdioSessionIO(SessionIO):
    """Translate session IO port calls to stdin/stdout."""

    def __init__(self, input_fn: InputFn = input, output_fn: OutputFn = print) -> None:
        self._input_fn = input_fn
        self._output_fn = output_fn

    def write_line(self, line: str) -> None:
        self._output_fn(line)

    def read_outcome(self, item: LearningItem) -> str:
        self._output_fn("Enter outcome [correct/c, incorrect/i, skip/s, quit/q]:")
        return self._input_fn()
