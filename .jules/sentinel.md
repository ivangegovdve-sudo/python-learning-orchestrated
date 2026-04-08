## 2025-02-23 - [JSON Parsing Unbounded Memory Consumption]
**Vulnerability:** Unbounded memory consumption DoS risk due to JSON file parsing without size limits in file-backed repositories and stores.
**Learning:** `json.loads(file.read_text())` reads the entire file content into memory. This can lead to out-of-memory errors or denial-of-service if an attacker or misconfiguration provides an excessively large file. The application relies heavily on file-backed adapters (e.g., `JsonFilePracticeRepository`, `JsonFileProgressSnapshotStore`, `CheckpointStore`).
**Prevention:** Implement a strict file size limit check using `path.stat().st_size` (e.g., standardized at 10MB or `10 * 1024 * 1024` bytes) before reading the file content into memory in all file-based adapters.

## 2024-02-23 - [Device File Size Read Bypass / TOCTOU]
**Vulnerability:** `path.stat().st_size` checks before `path.read_text()` are vulnerable to TOCTOU and bypass via device files (like `/dev/zero`), which report size 0 but produce infinite data.
**Learning:** To prevent unbounded memory consumption and DoS, verifying `path.is_file()` first is crucial. However, the most secure approach combines `path.is_file()` with a bounded read pattern (`f.read(limit + 1)`) instead of relying solely on `st_size` beforehand.
**Prevention:** Ensure file adapters always use `path.is_file()` to reject device files and perform bounded reads (`content = f.read(LIMIT + 1); if len(content) > LIMIT: raise ValueError(...)`) instead of relying on `path.stat().st_size`.
