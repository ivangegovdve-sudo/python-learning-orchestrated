"""Smoke and integration tests for CLI wiring to the interactive loop."""

from __future__ import annotations

import json
from pathlib import Path

from python_learning_orchestrated.cli import main


def test_cli_shows_startup_and_exits(capsys) -> None:
    """CLI should print startup info and exit when choosing 0."""
    main([], input_fn=lambda: "0")

    output = capsys.readouterr().out
    assert "Python Learning Orchestrated" in output
    assert "User: demo-user" in output
    assert "Progress:" in output
    assert "Goodbye!" in output


def test_cli_progress_file_resumes_progress(tmp_path, capsys) -> None:
    """CLI should persist progress and resume from it with --progress-file."""
    progress_file = tmp_path / "progress" / "state.json"

    choices = iter(["1", "0"])
    main(["--progress-file", str(progress_file)], input_fn=lambda: next(choices))
    first_output = capsys.readouterr().out

    choices = iter(["1", "0"])
    main(["--progress-file", str(progress_file)], input_fn=lambda: next(choices))
    second_output = capsys.readouterr().out

    assert "Completed lesson: variables" in first_output
    assert "Completed lesson: loops" in second_output
    assert Path(progress_file).exists()


def test_cli_session_command_runs_practice_loop(capsys) -> None:
    choices = iter(["correct", "quit"])

    main(["session"], input_fn=lambda: next(choices))

    output = capsys.readouterr().out
    assert "Starting practice session." in output
    assert "Activity variables-review" in output
    assert "Recorded: correct for variables-review." in output
    assert "Session ended by user." in output


def test_cli_export_and_import_progress_commands(tmp_path, capsys) -> None:
    session_file = tmp_path / "session.json"
    export_file = tmp_path / "export.json"

    choices = iter(["correct", "quit"])
    main(
        ["session", "--session-file", str(session_file)], input_fn=lambda: next(choices)
    )

    main(
        [
            "export-progress",
            "--session-file",
            str(session_file),
            "--out",
            str(export_file),
        ]
    )
    export_output = capsys.readouterr().out

    payload = json.loads(export_file.read_text(encoding="utf-8"))
    assert payload["version"] == 1
    assert len(payload["items"]) >= 2
    assert len(payload["attempts"]) == 1
    assert "Exported progress snapshot" in export_output

    main(
        [
            "import-progress",
            "--session-file",
            str(session_file),
            "--in",
            str(export_file),
        ]
    )
    import_output = capsys.readouterr().out
    assert "Imported progress snapshot" in import_output

    session_payload = json.loads(session_file.read_text(encoding="utf-8"))
    assert len(session_payload["attempts"]) == 1
