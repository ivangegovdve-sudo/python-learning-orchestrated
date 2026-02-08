"""Application lesson execution loop."""

from __future__ import annotations

from python_learning_orchestrated.application.progress_service import ProgressService
from python_learning_orchestrated.domain.learning_path import LearningPath


class LessonRunner:
    """Run the next available lesson for a learner and record completion."""

    def __init__(
        self,
        progress_service: ProgressService,
        learning_path: LearningPath,
    ) -> None:
        self._progress_service = progress_service
        self._learning_path = learning_path

    def run_next_lesson(self, user_id: str) -> dict[str, str | None]:
        """Complete the next uncompleted lesson and return its execution status."""
        progress = self._progress_service.get_user_progress(user_id)
        completed_lessons_value: object = progress.get("completed_lessons", [])

        if isinstance(completed_lessons_value, list):
            completed_lessons = completed_lessons_value
        else:
            completed_lessons = []

        completed_lesson_ids = [
            lesson_id for lesson_id in completed_lessons if isinstance(lesson_id, str)
        ]

        for lesson in self._learning_path.lessons:
            if lesson.id not in completed_lesson_ids:
                updated_completed_lessons = [*completed_lesson_ids, lesson.id]
                self._progress_service.record_user_progress(
                    user_id,
                    {
                        "lesson_id": lesson.id,
                        "status": "completed",
                        "completed_lessons": updated_completed_lessons,
                    },
                )
                return {"lesson_id": lesson.id, "status": "completed"}

        return {"lesson_id": None, "status": "completed_all"}
