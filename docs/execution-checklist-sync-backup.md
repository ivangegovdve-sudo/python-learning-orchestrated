# Execution Checklist — Device Sync & Backup Center (Critical Path Only)

- [ ] Lock scope to **manual backup/restore first**: `Export Progress` and `Import Progress` entry points in a new `Sync & Backup` menu, using existing transfer services unchanged.
- [ ] Add application-layer use cases for backup center actions that only orchestrate existing export/import flows and return user-facing statuses.
- [ ] Add thin CLI/UI wiring for the new menu/actions (no domain logic in CLI).
- [ ] Implement backup metadata recording (timestamp, file path, result) in an adapter-backed history store.
- [ ] Add `List Backups` + `Restore Selected Backup` flow using recorded history and existing import path.
- [ ] Add a **single safe default** conflict policy for restore (`replace current progress`) to avoid blocking UX decisions.
- [ ] Add focused tests for new application orchestration and adapter persistence paths.
- [ ] Ship PR1 when manual backup/restore + history browsing are usable end-to-end.
- [ ] Add scheduled backup orchestration (timer-triggered call to existing export use case).
- [ ] Expose schedule controls (enable/disable + interval + destination) in CLI/UI.
- [ ] Add failure-tolerant job behavior (log failure, keep app usable, retry next interval).
- [ ] Ship PR2 when scheduled backups create restorable snapshots visible in history.
- [ ] **Explicitly defer (non-blocking, no user harm now):** merge/preview conflict UI, dedupe of near-identical snapshots, encrypted backup files, cloud sync providers, cross-device live sync, granular retention policies, and rich backup analytics.
- [ ] **Explicitly ignore for now:** corrupted-file recovery wizard, partial-import reconciliation, timezone-localized schedule UX, and concurrent multi-process backup locking.
