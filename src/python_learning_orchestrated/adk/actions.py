from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
import json
from pathlib import Path
from typing import Any, Callable

from python_learning_orchestrated.adapters.in_memory_progress_repository import (
    InMemoryProgressRepository,
)
from python_learning_orchestrated.adapters.json_file_progress_repository import (
    JsonFileProgressRepository,
)
from python_learning_orchestrated.application.interactive_ui import progress_summary
from python_learning_orchestrated.application.lesson_runner import LessonRunner
from python_learning_orchestrated.application.progress_service import ProgressService
from python_learning_orchestrated.domain.learning_path import LearningPath, Lesson


ARTIFACTS_DIR = Path("data") / "adk_artifacts"


@dataclass(slots=True)
class ActionResult:
    action: str
    ok: bool
    summary: str
    artifacts: list[str] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)
    verification_notes: list[str] = field(default_factory=list)
    repaired: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


ActionFn = Callable[[Path, dict[str, Any]], ActionResult]
ValidatorFn = Callable[[Path, dict[str, Any], ActionResult], tuple[bool, list[str]]]


def execute_action(action_name: str, base_dir: Path, arguments: dict[str, Any]) -> ActionResult:
    return ACTIONS[action_name](base_dir, arguments)


def verify_action(
    action_name: str,
    base_dir: Path,
    arguments: dict[str, Any],
    result: ActionResult,
) -> tuple[bool, list[str]]:
    return VALIDATORS[action_name](base_dir, arguments, result)


def generate_progress_report(base_dir: Path, arguments: dict[str, Any]) -> ActionResult:
    user_id = arguments.get("user_id", "demo-user")
    progress_file = arguments.get("progress_file")
    output_name = arguments.get("output_name", "progress-report.json")
    service = _build_progress_service(progress_file)
    learning_path = _build_learning_path()
    completed_count, total_count = progress_summary(service, learning_path, user_id)
    payload = {
        "generated_at": datetime.now().isoformat(),
        "user_id": user_id,
        "completed_count": completed_count,
        "total_count": total_count,
        "progress": service.get_user_progress(user_id),
    }
    artifact_path = _artifact_path(base_dir, output_name)
    artifact_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return ActionResult(
        action="generate_progress_report",
        ok=True,
        summary=f"Wrote progress report for {user_id}: {completed_count}/{total_count} lessons complete.",
        artifacts=[str(artifact_path.relative_to(base_dir))],
        details=payload,
    )


def run_next_lesson(base_dir: Path, arguments: dict[str, Any]) -> ActionResult:
    user_id = arguments.get("user_id", "demo-user")
    progress_file = arguments.get("progress_file")
    service = _build_progress_service(progress_file)
    learning_path = _build_learning_path()
    runner = LessonRunner(service, learning_path)
    outcome = runner.run_next_lesson(user_id)
    return ActionResult(
        action="run_next_lesson",
        ok=True,
        summary=f"Ran next lesson for {user_id}: {outcome['status']}.",
        details={
            "lesson_id": outcome.get("lesson_id"),
            "status": outcome.get("status"),
            "progress": service.get_user_progress(user_id),
        },
    )


def validate_generate_progress_report(
    base_dir: Path,
    arguments: dict[str, Any],
    result: ActionResult,
) -> tuple[bool, list[str]]:
    artifact_path = _artifact_path(base_dir, arguments.get("output_name", "progress-report.json"))
    if not artifact_path.exists():
        return False, [f"Progress report artifact missing: {artifact_path}"]
    payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    required_keys = {"completed_count", "total_count", "user_id"}
    if not required_keys.issubset(payload):
        return False, ["Progress report is missing required keys."]
    return True, [f"Verified progress report for {payload['user_id']}."]


def validate_run_next_lesson(
    base_dir: Path,
    arguments: dict[str, Any],
    result: ActionResult,
) -> tuple[bool, list[str]]:
    progress = result.details.get("progress", {})
    completed_lessons = progress.get("completed_lessons", [])
    if not isinstance(completed_lessons, list) or not completed_lessons:
        return False, ["No completed lessons were recorded after the run."]
    if arguments.get("progress_file"):
        progress_path = base_dir / arguments["progress_file"]
        if not progress_path.exists():
            return False, [f"Progress file missing: {progress_path}"]
    return True, [f"Verified {len(completed_lessons)} completed lessons in progress."]


def _build_progress_service(progress_file: str | None) -> ProgressService:
    if progress_file:
        return ProgressService(JsonFileProgressRepository(progress_file))
    return ProgressService(InMemoryProgressRepository())


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


def _artifact_path(base_dir: Path, output_name: str) -> Path:
    target = base_dir / ARTIFACTS_DIR / output_name
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


ACTIONS: dict[str, ActionFn] = {
    "generate_progress_report": generate_progress_report,
    "run_next_lesson": run_next_lesson,
}

VALIDATORS: dict[str, ValidatorFn] = {
    "generate_progress_report": validate_generate_progress_report,
    "run_next_lesson": validate_run_next_lesson,
}
