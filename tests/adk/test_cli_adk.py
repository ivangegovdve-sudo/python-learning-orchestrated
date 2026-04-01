from __future__ import annotations

import json

from python_learning_orchestrated.cli import main


def test_cli_adk_roadmap_outputs_json(capsys) -> None:
    main(["adk-roadmap", "--json"])

    payload = json.loads(capsys.readouterr().out)
    assert payload["title"].startswith("Python Learning Orchestrated")
    assert payload["tasks"]


def test_cli_adk_run_next_outputs_json(tmp_path, capsys) -> None:
    progress_file = tmp_path / "progress.json"
    roadmap_copy = tmp_path / "adk-roadmap.md"
    roadmap_copy.write_text(
        (
            "# Test Roadmap\n\n"
            "### `step-1` - Run lesson\n"
            "Status: todo\n"
            "Depends on: none\n"
            "Action: run_next_lesson\n"
            f"Arguments: {{\"progress_file\":\"{progress_file.as_posix()}\",\"user_id\":\"demo-user\"}}\n"
            "Success criteria:\n"
            "- A lesson is completed.\n"
            "Verification:\n"
            "- Progress is persisted.\n"
        ),
        encoding="utf-8",
    )

    main(["adk-run-next", "--json", "--roadmap-file", str(roadmap_copy)])

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "done"
    assert payload["task"]["id"] == "step-1"
