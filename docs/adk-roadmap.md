# Python Learning Orchestrated ADK Roadmap

### `baseline-progress-report` - Capture a baseline learner progress report
Status: todo
Depends on: none
Action: generate_progress_report
Arguments: {"output_name":"baseline-progress.json","progress_file":"data/adk-progress.json","user_id":"demo-user"}
Success criteria:
- A progress report artifact is written for the learner.
- The report includes completed and total lesson counts.
Verification:
- The report exists under `data/adk_artifacts`.
- The report JSON contains `completed_count` and `total_count`.

### `complete-next-lesson` - Complete the next lesson for the learner
Status: todo
Depends on: baseline-progress-report
Action: run_next_lesson
Arguments: {"progress_file":"data/adk-progress.json","user_id":"demo-user"}
Success criteria:
- The next unfinished lesson is marked complete for the learner.
- Progress persists in the configured progress file.
Verification:
- The progress file exists.
- The learner has at least one completed lesson recorded.

### `follow-up-progress-report` - Capture a follow-up report after lesson execution
Status: todo
Depends on: complete-next-lesson
Action: generate_progress_report
Arguments: {"output_name":"follow-up-progress.json","progress_file":"data/adk-progress.json","user_id":"demo-user"}
Success criteria:
- A second progress report artifact is written after lesson completion.
- The report reflects the learner's updated progress.
Verification:
- The follow-up report exists under `data/adk_artifacts`.
- The follow-up report shows at least one completed lesson.
