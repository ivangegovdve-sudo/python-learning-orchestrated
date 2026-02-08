# Next-step features unlocked by reliable progress export/import

With progress export/import now reliable, we can build user-visible capabilities that treat progress as a portable product asset. Below are three large follow-on features that explicitly *reuse* existing export/import behavior without changing that core mechanism.

## 1) Device Sync & Backup Center

### User value
- Users can move between laptop/desktop environments without losing continuity.
- A single “Backup & Restore” workflow reduces fear of data loss.
- Users can recover quickly after reinstalling, switching machines, or accidental resets.

### New surface area introduced
- **New UI flow:** “Sync & Backup” menu/screen with actions like `Export Progress`, `Import Progress`, `Create Scheduled Backup`, and `Restore from Backup`.
- **New scheduling/automation layer:** local timed backup jobs that trigger existing export APIs to a user-selected folder.
- **Conflict-resolution UX:** when importing into a non-empty profile, show choice prompts (replace, keep both snapshots, preview differences).
- **History browser:** list of backup snapshots with timestamps and metadata for restore selection.

### Why this is a big step (not a refinement)
- It turns progress portability into a first-class lifecycle feature (capture, retain, recover), not just a technical utility.
- It creates persistent trust and retention benefits: users are willing to invest more in learning when progress safety is obvious.
- It introduces a new user journey and operational behavior (scheduled backups + restore management) beyond current session workflows.

### Delivery scope (<= 2 focused PRs)
1. **PR1:** Add Sync & Backup Center UI and manual export/import entry points using existing transfer calls.
2. **PR2:** Add scheduled backup orchestration + backup history/restore UX, still delegating data movement to existing export/import.

---

## 2) Mentor/Coach Review Pack Sharing

### User value
- Learners can share a progress pack with a mentor/coach/tutor for structured feedback.
- Coaches can import learner packs to review completion patterns and assign targeted next steps.
- Enables lightweight accountability loops without requiring a shared live database.

### New surface area introduced
- **Share action in product:** “Generate Review Pack” (export + optional note + date range selector).
- **Coach-facing import workflow:** “Open Learner Pack” with read-only review mode.
- **Annotation surface:** coach comments/recommendations attached to lessons/skills and exported as a response pack.
- **Return channel UX:** learner imports mentor response pack to see recommendations inline.

### Why this is a big step (not a refinement)
- It shifts the app from single-player self-tracking to collaborative learning.
- It introduces an ecosystem role (mentor/coach) with distinct workflows and value.
- It creates a bidirectional artifact loop (learner export -> coach import/review -> coach export -> learner import), all user-visible and behaviorally new.

### Delivery scope (<= 2 focused PRs)
1. **PR1:** Learner review-pack creation + coach read-only import/review view.
2. **PR2:** Coach annotations + response-pack export and learner-side import/rendering.

---

## 3) Team Challenge Events (Import-Based Leaderboards)

### User value
- Groups (class cohort, study club, company cohort) can run time-boxed challenges with visible standings.
- Learners gain motivation through social progress and milestone badges.
- Organizers can collect participant progress files and publish leaderboard snapshots.

### New surface area introduced
- **Organizer workflow:** “Create Challenge” with rules (date window, metrics, scoring model).
- **Participant flow:** “Submit Progress Snapshot” (export file generated and uploaded/shared externally).
- **Leaderboard UI:** ranking table, streak indicators, challenge badges, and periodic snapshot refresh.
- **Challenge report export:** end-of-event results package for participants.

### Why this is a big step (not a refinement)
- It introduces multi-user, event-driven product behavior and social mechanics.
- It creates a new outcome: comparative performance and shared milestones, not just personal tracking.
- It opens organizational use cases (bootcamps/classes/teams) that materially expand product scope and adoption.

### Delivery scope (<= 2 focused PRs)
1. **PR1:** Challenge configuration + participant submission/import pipeline + basic leaderboard.
2. **PR2:** Badges/streak overlays + final challenge report generation and publishing UI.
