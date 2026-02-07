"""Unit tests for learning path domain models."""

from python_learning_orchestrated.domain.learning_path import LearningPath, Lesson


def test_learning_path_adds_lessons_in_order() -> None:
    path = LearningPath(
        id="lp-1",
        title="Python Basics",
        description="A starter learning path for Python fundamentals.",
    )

    lesson_one = Lesson(
        id="lesson-1",
        title="Variables",
        content="Learn how to declare and use variables.",
    )
    lesson_two = Lesson(
        id="lesson-2",
        title="Control Flow",
        content="Learn conditionals and loops.",
    )

    path.add_lesson(lesson_one)
    path.add_lesson(lesson_two)

    assert [lesson.id for lesson in path.lessons] == ["lesson-1", "lesson-2"]
    assert path.lessons[0].title == "Variables"
    assert path.lessons[1].content == "Learn conditionals and loops."
    assert path.title == "Python Basics"
