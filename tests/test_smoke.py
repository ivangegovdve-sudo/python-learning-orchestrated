"""Smoke tests for initial package scaffold."""

from python_learning_orchestrated import greet


def test_greet_default_message() -> None:
    assert "Welcome to Python Learning Orchestrated" in greet()


def test_greet_custom_name() -> None:
    assert greet("Ada") == "Hello, Ada! Welcome to Python Learning Orchestrated."
