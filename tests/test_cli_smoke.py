"""Smoke test for CLI wiring to the lesson runner."""

from python_learning_orchestrated.cli import main


def test_cli_prints_demo_user_lesson_run(capsys) -> None:
    """CLI should print lesson execution result from the runner."""
    main()

    output = capsys.readouterr().out
    assert "lesson_id" in output
    assert "variables" in output
    assert "status" in output
    assert "completed" in output
