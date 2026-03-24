## 2025-02-23 - [JSON Parsing Unbounded Memory Consumption]
**Vulnerability:** Unbounded memory consumption DoS risk due to JSON file parsing without size limits in file-backed repositories and stores.
**Learning:** `json.loads(file.read_text())` reads the entire file content into memory. This can lead to out-of-memory errors or denial-of-service if an attacker or misconfiguration provides an excessively large file. The application relies heavily on file-backed adapters (e.g., `JsonFilePracticeRepository`, `JsonFileProgressSnapshotStore`, `CheckpointStore`).
**Prevention:** Implement a strict file size limit check using `path.stat().st_size` (e.g., standardized at 10MB or `10 * 1024 * 1024` bytes) before reading the file content into memory in all file-based adapters.
## 2025-02-23 - [TOCTOU Vulnerability in File Size Checks]
**Vulnerability:** Time-of-Check to Time-of-Use (TOCTOU) and Device File Bypass in file size limits.
**Learning:** Checking `path.stat().st_size` is vulnerable to TOCTOU if the file changes between stat and read. Furthermore, checking `st_size` on device files (like `/dev/zero`) returns 0, bypassing the size check, and `read_text()` will then consume unbounded memory.
**Prevention:** To prevent unbounded memory consumption and TOCTOU, JSON file-backed adapters must use a secure bounded read pattern. Open the file, read up to `limit + 1` bytes, and raise `ValueError` if the length of the read content exceeds the limit. Do not rely solely on `st_size`.
