"""Smoke and integration tests for CLI wiring to the lesson runner."""

from __future__ import annotations

from pathlib import Path

from python_learning_orchestrated.cli import main


def test_cli_prints_demo_user_lesson_run(capsys) -> None:
    """CLI should print lesson execution result from the runner."""
    main([])

    output = capsys.readouterr().out
    assert "lesson_id" in output
    assert "variables" in output
    assert "status" in output
    assert "completed" in output


def test_cli_progress_file_resumes_progress(tmp_path, capsys) -> None:
    """CLI should persist progress and resume from it with --progress-file."""
    progress_file = tmp_path / "progress" / "state.json"

    main(["--progress-file", str(progress_file)])
    first_output = capsys.readouterr().out

    main(["--progress-file", str(progress_file)])
    second_output = capsys.readouterr().out

    assert "variables" in first_output
    assert "loops" in second_output
    assert Path(progress_file).exists()
