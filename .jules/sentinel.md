## 2025-02-23 - [JSON Parsing Unbounded Memory Consumption]
**Vulnerability:** Unbounded memory consumption DoS risk due to JSON file parsing without size limits in file-backed repositories and stores.
**Learning:** `json.loads(file.read_text())` reads the entire file content into memory. This can lead to out-of-memory errors or denial-of-service if an attacker or misconfiguration provides an excessively large file. The application relies heavily on file-backed adapters (e.g., `JsonFilePracticeRepository`, `JsonFileProgressSnapshotStore`, `CheckpointStore`).
**Prevention:** Implement a strict file size limit check using `path.stat().st_size` (e.g., standardized at 10MB or `10 * 1024 * 1024` bytes) before reading the file content into memory in all file-based adapters.

## 2025-02-23 - [TOCTOU and DoS via File Stat Checks]
**Vulnerability:** Using `path.stat().st_size` to check file size limits before reading the entire file (TOCTOU), and using `.exists()` instead of `.is_file()`, which allows device files (like `/dev/zero`) to report a size of 0 and bypass the check, leading to unbounded memory consumption DoS.
**Learning:** Checking size before reading is susceptible to Time-of-Check to Time-of-Use race conditions if the file is modified in between. Furthermore, device files report incorrect sizes, circumventing the limit entirely if `.exists()` is used instead of `.is_file()`.
**Prevention:** Always verify a path is a regular file using `path.is_file()` first. To prevent TOCTOU when enforcing size limits, implement a secure bounded read (e.g., `content = f.read(limit + 1)`) and raise a ValueError if the returned length exceeds the limit, rather than relying on pre-read stat checks.
