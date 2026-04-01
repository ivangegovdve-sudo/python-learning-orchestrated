from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

from google.adk import Agent
from google.adk.apps import App
from google.adk.plugins import LoggingPlugin, ReflectAndRetryToolPlugin

from python_learning_orchestrated.adapters.json_file_practice_repository import (
    JsonFilePracticeRepository,
)
from python_learning_orchestrated.adapters.json_file_progress_repository import (
    JsonFileProgressRepository,
)
from python_learning_orchestrated.adapters.json_file_progress_snapshot_store import (
    JsonFileProgressSnapshotStore,
)
from python_learning_orchestrated.application.lesson_runner import LessonRunner
from python_learning_orchestrated.application.progress_service import ProgressService
from python_learning_orchestrated.application.progress_transfer import (
    ExportProgress,
    ImportProgress,
)
from python_learning_orchestrated.domain.learning_path import LearningPath, Lesson
from python_learning_orchestrated.domain.practice import LearningItem
from python_learning_orchestrated.adk.roadmap import load_roadmap
from python_learning_orchestrated.adk.workflow import LocalWorkflowEngine


def build_app(base_dir: Path | None = None) -> App:
    repo_root = base_dir or Path(__file__).resolve().parents[3]
    model_name = os.environ.get("ADK_MODEL", "gemini-2.5-flash")
    roadmap_path = repo_root / "docs" / "adk-roadmap.md"
    history_path = repo_root / "data" / "adk_runs.json"

    def get_user_progress(progress_file: str = "data/adk-progress.json", user_id: str = "demo-user") -> dict:
        """Return persisted learner progress for a user."""
        service = ProgressService(JsonFileProgressRepository(progress_file))
        return {"user_id": user_id, "progress": service.get_user_progress(user_id)}

    def run_next_lesson_for_user(progress_file: str = "data/adk-progress.json", user_id: str = "demo-user") -> dict:
        """Run the next lesson for a learner and persist the updated progress."""
        service = ProgressService(JsonFileProgressRepository(progress_file))
        runner = LessonRunner(service, _build_learning_path())
        return runner.run_next_lesson(user_id)

    def reset_user_progress(progress_file: str = "data/adk-progress.json", user_id: str = "demo-user") -> dict:
        """Reset persisted progress for a learner."""
        service = ProgressService(JsonFileProgressRepository(progress_file))
        service.reset_user_progress(user_id)
        return {"user_id": user_id, "status": "reset"}

    def export_progress_snapshot(
        session_file: str = "data/adk-session.json",
        output_file: str = "data/adk-progress-snapshot.json",
    ) -> dict:
        """Export practice-session progress into a snapshot file."""
        repository = JsonFilePracticeRepository(session_file, _build_practice_items())
        snapshot = ExportProgress(
            repository=repository,
            now_provider=datetime.now,
        ).run()
        JsonFileProgressSnapshotStore(output_file).save(snapshot)
        return {"output_file": output_file, "item_count": len(snapshot.items)}

    def import_progress_snapshot(
        session_file: str = "data/adk-session.json",
        input_file: str = "data/adk-progress-snapshot.json",
    ) -> dict:
        """Import a practice-session progress snapshot."""
        repository = JsonFilePracticeRepository(session_file, _build_practice_items())
        snapshot = JsonFileProgressSnapshotStore(input_file).load()
        merged = ImportProgress(repository=repository).run(snapshot)
        return {"input_file": input_file, "item_count": len(merged.items)}

    def list_roadmap_tasks() -> dict:
        """Return the checked-in roadmap used by the local workflow engine."""
        return load_roadmap(roadmap_path).to_dict()

    def run_next_roadmap_task(
        progress_file: str = "data/adk-progress.json",
        session_file: str = "data/adk-session.json",
    ) -> dict:
        """Run the next eligible roadmap task for this repository."""
        engine = LocalWorkflowEngine(
            repo_name="python-learning-orchestrated",
            base_dir=repo_root,
            roadmap_path=roadmap_path,
            history_path=history_path,
        )
        return engine.run_next()

    executor_agent = Agent(
        name="executor",
        model=model_name,
        description="Executes the next roadmap or learner task.",
        instruction=(
            "Advance the learner state using the concrete tools. Prefer running the next "
            "roadmap task when asked to move the project forward."
        ),
        tools=[
            get_user_progress,
            run_next_lesson_for_user,
            export_progress_snapshot,
            list_roadmap_tasks,
            run_next_roadmap_task,
        ],
    )

    verifier_agent = Agent(
        name="verifier_fixer",
        model=model_name,
        description="Verifies learner progress state and can repair or reset it.",
        instruction=(
            "Check whether learner progress and roadmap state look correct. Use the "
            "reset or import tools only when the user explicitly wants repair."
        ),
        tools=[
            get_user_progress,
            reset_user_progress,
            import_progress_snapshot,
            list_roadmap_tasks,
        ],
    )

    root_agent = Agent(
        name="python_learning_orchestrator",
        model=model_name,
        description="Coordinates roadmap execution and learner progress workflows.",
        instruction=(
            "Coordinate the executor and verifier_fixer agents to move the learner "
            "forward one safe step at a time."
        ),
        sub_agents=[executor_agent, verifier_agent],
        tools=[list_roadmap_tasks],
    )

    return App(
        name="python_learning_adk_app",
        root_agent=root_agent,
        plugins=[LoggingPlugin(), ReflectAndRetryToolPlugin(max_retries=2)],
    )


def _build_learning_path() -> LearningPath:
    return LearningPath(
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


def _build_practice_items() -> list[LearningItem]:
    return [
        LearningItem(
            id="variables-review",
            prompt="What is a variable in Python?",
            status="new",
            order=1,
        ),
        LearningItem(
            id="loops-review",
            prompt="When would you use a for loop?",
            status="new",
            order=2,
        ),
    ]
