"""Smoke and integration tests for CLI wiring to the interactive loop."""

from __future__ import annotations

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
