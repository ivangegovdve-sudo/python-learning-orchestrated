"""Text-based interactive UI loop for the learning app."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from python_learning_orchestrated.application.lesson_runner import LessonRunner
from python_learning_orchestrated.application.progress_service import ProgressService
from python_learning_orchestrated.domain.learning_path import LearningPath

InputFn = Callable[[], str]
OutputFn = Callable[[str], None]


@dataclass(frozen=True, slots=True)
class MenuActionResult:
    """Result payload for a menu action."""

    lines: list[str]
    should_exit: bool = False


class InteractiveLearningUI:
    """Coordinate rendering and menu actions for the interactive app loop."""

    def __init__(
        self,
        user_id: str,
        progress_service: ProgressService,
        lesson_runner: LessonRunner,
        learning_path: LearningPath,
    ) -> None:
        self._user_id = user_id
        self._progress_service = progress_service
        self._lesson_runner = lesson_runner
        self._learning_path = learning_path

    def startup_lines(self) -> list[str]:
        """Build startup text with title, user id, and progress summary."""
        completed_count, total_count = progress_summary(
            self._progress_service,
            self._learning_path,
            self._user_id,
        )
        return [
            "=== Python Learning Orchestrated ===",
            f"User: {self._user_id}",
            f"Progress: {completed_count}/{total_count} lessons completed",
        ]

    def menu_lines(self) -> list[str]:
        """Build menu options text."""
        return [
            "",
            "[1] Start / Continue learning",
            "[2] Show progress",
            "[3] Reset progress",
            "[0] Exit",
        ]

    def handle_menu_choice(self, choice: str) -> MenuActionResult:
        """Execute a menu action for a raw user choice string."""
        normalized = choice.strip()

        if normalized == "1":
            return start_or_continue_learning(
                self._lesson_runner,
                self._progress_service,
                self._learning_path,
                self._user_id,
            )
        if normalized == "2":
            return show_progress(
                self._progress_service,
                self._learning_path,
                self._user_id,
            )
        if normalized == "3":
            return reset_progress(self._progress_service, self._user_id)
        if normalized == "0":
            return MenuActionResult(lines=["Goodbye!"], should_exit=True)

        return MenuActionResult(lines=["Invalid choice. Please select 0, 1, 2, or 3."])


def progress_summary(
    progress_service: ProgressService,
    learning_path: LearningPath,
    user_id: str,
) -> tuple[int, int]:
    """Return completed and total lesson counts for user."""
    completed_ids = _completed_lesson_ids(progress_service, user_id)
    total_count = len(learning_path.lessons)
    completed_count = sum(1 for lesson in learning_path.lessons if lesson.id in completed_ids)
    return completed_count, total_count


def start_or_continue_learning(
    lesson_runner: LessonRunner,
    progress_service: ProgressService,
    learning_path: LearningPath,
    user_id: str,
) -> MenuActionResult:
    """Run next incomplete lesson and return status lines."""
    result = lesson_runner.run_next_lesson(user_id)
    status = result.get("status")
    lesson_id = result.get("lesson_id")

    lines: list[str]
    if status == "completed" and isinstance(lesson_id, str):
        completed_count, total_count = progress_summary(
            progress_service,
            learning_path,
            user_id,
        )
        lines = [
            f"Completed lesson: {lesson_id}",
            f"Progress: {completed_count}/{total_count} lessons completed",
        ]
    else:
        lines = ["All lessons are already completed."]

    return MenuActionResult(lines=lines)


def show_progress(
    progress_service: ProgressService,
    learning_path: LearningPath,
    user_id: str,
) -> MenuActionResult:
    """List lessons with completed/pending status for current user."""
    completed_ids = _completed_lesson_ids(progress_service, user_id)

    lines = ["Progress by lesson:"]
    for lesson in learning_path.lessons:
        status = "completed" if lesson.id in completed_ids else "pending"
        lines.append(f"- {lesson.id}: {status}")

    return MenuActionResult(lines=lines)


def reset_progress(progress_service: ProgressService, user_id: str) -> MenuActionResult:
    """Clear persisted progress for current user only."""
    progress_service.reset_user_progress(user_id)
    return MenuActionResult(lines=[f"Progress reset for user: {user_id}"])


def run_interactive_ui_loop(
    ui: InteractiveLearningUI,
    input_fn: InputFn = input,
    output_fn: OutputFn = print,
) -> None:
    """Run interactive menu loop until the user exits."""
    for line in ui.startup_lines():
        output_fn(line)

    while True:
        for line in ui.menu_lines():
            output_fn(line)

        output_fn("")
        output_fn("Select an option:")
        choice = input_fn()

        action_result = ui.handle_menu_choice(choice)
        output_fn("")
        for line in action_result.lines:
            output_fn(line)

        if action_result.should_exit:
            return


def _completed_lesson_ids(progress_service: ProgressService, user_id: str) -> set[str]:
    progress = progress_service.get_user_progress(user_id)
    completed_lessons_value: object = progress.get("completed_lessons", [])

    if not isinstance(completed_lessons_value, list):
        return set()

    return {
        lesson_id
        for lesson_id in completed_lessons_value
        if isinstance(lesson_id, str)
    }
