## 2025-02-23 - [JSON Parsing Unbounded Memory Consumption]
**Vulnerability:** Unbounded memory consumption DoS risk due to JSON file parsing without size limits in file-backed repositories and stores.
**Learning:** `json.loads(file.read_text())` reads the entire file content into memory. This can lead to out-of-memory errors or denial-of-service if an attacker or misconfiguration provides an excessively large file. The application relies heavily on file-backed adapters (e.g., `JsonFilePracticeRepository`, `JsonFileProgressSnapshotStore`, `CheckpointStore`).
**Prevention:** Implement a strict file size limit check using `path.stat().st_size` (e.g., standardized at 10MB or `10 * 1024 * 1024` bytes) before reading the file content into memory in all file-based adapters.

## 2024-05-18 - [TOCTOU in file size limit checking]
**Vulnerability:** Checking file size using `path.stat().st_size` prior to reading is vulnerable to Time-Of-Check to Time-Of-Use (TOCTOU) and out-of-memory DoS, as well as bypassing checks via device files like `/dev/zero` which report size 0.
**Learning:** `path.exists()` or `path.stat().st_size` checks the state of the filesystem. By the time the file is read, the file could have been changed, or a different file type like a device file could have been placed there, evading the check.
**Prevention:** Verify it's a regular file first (`path.is_file()`), then read with a strict bound like `f.read(limit + 1)`, and if the read returned size is strictly greater than the limit, throw a size limit exception.
