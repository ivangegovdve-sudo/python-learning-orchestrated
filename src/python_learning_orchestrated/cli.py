"""Command-line entrypoint for the project."""

from python_learning_orchestrated.adapters.in_memory_progress_repository import (
    InMemoryProgressRepository,
)
from python_learning_orchestrated.application.progress_service import ProgressService


def main() -> None:
    """Run a minimal CLI flow that records and prints demo user progress."""
    user_id = "demo-user"
    repository = InMemoryProgressRepository()
    service = ProgressService(repository)

    sample_progress: dict[str, object] = {
        "lesson_id": "variables",
        "completed": True,
    }
    service.record_user_progress(user_id, sample_progress)

    progress = service.get_user_progress(user_id)
    print(progress)


if __name__ == "__main__":
    main()
