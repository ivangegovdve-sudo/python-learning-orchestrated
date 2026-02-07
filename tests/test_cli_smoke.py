"""Smoke test for CLI wiring to the progress service."""

from python_learning_orchestrated.cli import main


def test_cli_prints_demo_user_progress(capsys) -> None:
    """CLI should print the sample progress loaded from the service."""
    main()

    output = capsys.readouterr().out
    assert "lesson_id" in output
    assert "variables" in output
    assert "completed" in output
    assert "True" in output
