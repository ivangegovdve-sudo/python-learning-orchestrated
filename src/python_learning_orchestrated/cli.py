"""Command-line entrypoint for the project."""

from __future__ import annotations

import argparse
from collections.abc import Callable
from datetime import datetime

from python_learning_orchestrated.adapters.checkpoint_store import CheckpointStore
from python_learning_orchestrated.adapters.in_memory_practice_repository import (
    InMemoryPracticeRepository,
)
from python_learning_orchestrated.adapters.in_memory_progress_repository import (
    InMemoryProgressRepository,
)
from python_learning_orchestrated.adapters.json_file_practice_repository import (
    JsonFilePracticeRepository,
)
from python_learning_orchestrated.adapters.json_file_progress_repository import (
    JsonFileProgressRepository,
)
from python_learning_orchestrated.adapters.json_file_progress_snapshot_store import (
    JsonFileProgressSnapshotStore,
)
from python_learning_orchestrated.adapters.stdio_session_io import StdioSessionIO
from python_learning_orchestrated.application.interactive_ui import (
    InteractiveLearningUI,
    run_interactive_ui_loop,
)
from python_learning_orchestrated.application.lesson_runner import LessonRunner
from python_learning_orchestrated.application.practice_session import RunPracticeSession
from python_learning_orchestrated.application.progress_service import ProgressService
from python_learning_orchestrated.application.progress_transfer import (
    ExportProgress,
    ImportProgress,
)
from python_learning_orchestrated.domain.learning_path import LearningPath, Lesson
from python_learning_orchestrated.domain.practice import LearningItem
from python_learning_orchestrated.ports.practice_repository import PracticeRepository
from python_learning_orchestrated.ports.progress_repository import ProgressRepository

InputFn = Callable[[], str]
OutputFn = Callable[[str], None]


def _build_parser() -> argparse.ArgumentParser:
    """Create CLI argument parser."""
    parser = argparse.ArgumentParser(description="Run python learning orchestrator")
    parser.add_argument(
        "--progress-file",
        type=str,
        default=None,
        help="Persist user progress in the given JSON file path.",
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="interactive",
        choices=[
            "interactive",
            "session",
            "export-progress",
            "import-progress",
            "checkpoint",
        ],
        help=(
            "Run interactive lesson menu, practice session, "
            "or progress transfer commands."
        ),
    )
    parser.add_argument(
        "checkpoint_command",
        nargs="?",
        default=None,
        choices=["create", "list"],
        help="Checkpoint action to run when command is checkpoint.",
    )
    parser.add_argument(
        "checkpoint_name",
        nargs="?",
        default=None,
        help="Checkpoint name used by checkpoint create.",
    )
    parser.add_argument(
        "--session-file",
        type=str,
        default=None,
        help="Persist practice session state in the given JSON file path.",
    )
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Output file for export-progress snapshot JSON.",
    )
    parser.add_argument(
        "--in",
        dest="input_path",
        type=str,
        default=None,
        help="Input file for import-progress snapshot JSON.",
    )
    return parser


def _build_repository(progress_file: str | None) -> ProgressRepository:
    """Create repository adapter from CLI options."""
    if progress_file:
        return JsonFileProgressRepository(progress_file)
    return InMemoryProgressRepository()


def _build_learning_path() -> LearningPath:
    """Build static learning path for the CLI experience."""
    return LearningPath(
        id="python-basics",
        title="Python Basics",
        description="A starter learning path for Python fundamentals.",
        lessons=[
            Lesson(
                id="variables",
                title="Variables",
                content="Learn how to declare and use variables.",
            ),
            Lesson(
                id="loops",
                title="Loops",
                content="Learn how to iterate with for and while loops.",
            ),
        ],
    )


def _build_practice_items() -> list[LearningItem]:
    return [
        LearningItem(
            id="variables-review",
            prompt="What is a variable in Python?",
            status="new",
            order=1,
        ),
        LearningItem(
            id="loops-review",
            prompt="When would you use a for loop?",
            status="new",
            order=2,
        ),
    ]


def _build_practice_repository(session_file: str | None) -> PracticeRepository:
    seed_items = _build_practice_items()
    if session_file:
        return JsonFilePracticeRepository(session_file, seed_items)
    return InMemoryPracticeRepository(seed_items)


def main(
    argv: list[str] | None = None,
    *,
    input_fn: InputFn = input,
    output_fn: OutputFn = print,
) -> None:
    """Run the text-based interactive learning loop."""
    args = _build_parser().parse_args(argv)

    if args.command == "session":
        repository = _build_practice_repository(args.session_file)
        io = StdioSessionIO(input_fn=input_fn, output_fn=output_fn)
        session = RunPracticeSession(
            repository=repository, io=io, now_provider=datetime.now
        )
        session.run()
        return

    if args.command == "export-progress":
        if not args.out:
            raise SystemExit("export-progress requires --out <file>")
        repository = _build_practice_repository(args.session_file)
        snapshot = ExportProgress(
            repository=repository, now_provider=datetime.now
        ).run()
        JsonFileProgressSnapshotStore(args.out).save(snapshot)
        output_fn(f"Exported progress snapshot to {args.out}.")
        return

    if args.command == "import-progress":
        if not args.input_path:
            raise SystemExit("import-progress requires --in <file>")
        repository = _build_practice_repository(args.session_file)
        snapshot = JsonFileProgressSnapshotStore(args.input_path).load()
        merged = ImportProgress(repository=repository).run(snapshot)
        output_fn(
            "Imported progress snapshot from "
            f"{args.input_path} ({len(merged.items)} items, "
            f"{len(merged.attempts)} attempts)."
        )
        return

    if args.command == "checkpoint":
        repository = _build_practice_repository(args.session_file)
        checkpoint_store = CheckpointStore()

        if args.checkpoint_command == "create":
            if not args.checkpoint_name:
                raise SystemExit("checkpoint create requires <name>")
            if any(
                checkpoint.name == args.checkpoint_name
                for checkpoint in checkpoint_store.list_checkpoints()
            ):
                raise SystemExit(f"checkpoint '{args.checkpoint_name}' already exists")
            snapshot = ExportProgress(
                repository=repository, now_provider=datetime.now
            ).run()
            checkpoint_store.save_checkpoint(args.checkpoint_name, snapshot)
            output_fn(f"Created checkpoint '{args.checkpoint_name}'.")
            return

        if args.checkpoint_command == "list":
            checkpoints = checkpoint_store.list_checkpoints()
            if not checkpoints:
                output_fn("No checkpoints found.")
                return
            output_fn("Checkpoints:")
            for checkpoint in checkpoints:
                output_fn(f"- {checkpoint.name} ({checkpoint.created_at.isoformat()})")
            return

        raise SystemExit("checkpoint requires create or list")

    user_id = "demo-user"
    progress_repository = _build_repository(args.progress_file)
    service = ProgressService(progress_repository)
    learning_path = _build_learning_path()
    runner = LessonRunner(service, learning_path)
    ui = InteractiveLearningUI(user_id, service, runner, learning_path)

    run_interactive_ui_loop(ui, input_fn=input_fn, output_fn=output_fn)


if __name__ == "__main__":
    main()
