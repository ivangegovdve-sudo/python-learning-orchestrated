"""Command-line entrypoint for the project."""

from python_learning_orchestrated import greet


def main() -> None:
    """Run the minimal CLI for Phase 1."""
    print(greet())


if __name__ == "__main__":
    main()
