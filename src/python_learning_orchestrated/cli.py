"""Command-line entrypoint for the project."""

from python_learning_orchestrated.adapters.in_memory_progress_repository import (
    InMemoryProgressRepository,
)
from python_learning_orchestrated.application.lesson_runner import LessonRunner
from python_learning_orchestrated.application.progress_service import ProgressService
from python_learning_orchestrated.domain.learning_path import LearningPath, Lesson


def main() -> None:
    """Run a minimal CLI flow that executes the next lesson."""
    user_id = "demo-user"
    repository = InMemoryProgressRepository()
    service = ProgressService(repository)
    learning_path = LearningPath(
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

    runner = LessonRunner(service, learning_path)
    result = runner.run_next_lesson(user_id)
    print(result)


if __name__ == "__main__":
    main()
