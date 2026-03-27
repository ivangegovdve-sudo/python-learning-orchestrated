## 2025-02-23 - [JSON Parsing Unbounded Memory Consumption]
**Vulnerability:** Unbounded memory consumption DoS risk due to JSON file parsing without size limits in file-backed repositories and stores.
**Learning:** `json.loads(file.read_text())` reads the entire file content into memory. This can lead to out-of-memory errors or denial-of-service if an attacker or misconfiguration provides an excessively large file. The application relies heavily on file-backed adapters (e.g., `JsonFilePracticeRepository`, `JsonFileProgressSnapshotStore`, `CheckpointStore`).
**Prevention:** Implement a strict file size limit check using `path.stat().st_size` (e.g., standardized at 10MB or `10 * 1024 * 1024` bytes) before reading the file content into memory in all file-based adapters.

## 2026-03-21 - [TOCTOU and Device File DoS bypass]
**Vulnerability:** Using `path.stat().st_size` to verify file size limits is vulnerable to Time-of-Check to Time-of-Use (TOCTOU) race conditions, and bypasses when encountering device files (like `/dev/zero`) which incorrectly report a 0 byte size but provide unbounded data streams.
**Learning:** Checking a file's size with `stat()` before opening it allows an attacker to swap the file between check and read. Also, special files don't accurately report their stream size through `stat()`, causing OOM crashes despite limit checks.
**Prevention:** Instead of `stat()`, check if the file is a regular file using `path.is_file()` first, then use a bounded read (e.g., `f.read(LIMIT + 1)`) while the file is already open to safely detect exceeding limits without risking OOM or race conditions.
