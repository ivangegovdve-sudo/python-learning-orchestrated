from __future__ import annotations

import json

from python_learning_orchestrated.adk.actions import generate_progress_report, run_next_lesson


def test_generate_progress_report_writes_artifact(tmp_path) -> None:
    result = generate_progress_report(
        tmp_path,
        {
            "progress_file": str(tmp_path / "progress.json"),
            "output_name": "report.json",
            "user_id": "demo-user",
        },
    )

    artifact_path = tmp_path / "data" / "adk_artifacts" / "report.json"
    payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert result.ok is True
    assert payload["user_id"] == "demo-user"
    assert payload["total_count"] == 2


def test_run_next_lesson_records_completed_lesson(tmp_path) -> None:
    progress_file = tmp_path / "progress.json"

    result = run_next_lesson(
        tmp_path,
        {
            "progress_file": str(progress_file),
            "user_id": "demo-user",
        },
    )

    assert result.ok is True
    assert result.details["lesson_id"] == "variables"
