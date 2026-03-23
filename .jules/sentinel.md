## 2025-02-23 - [JSON Parsing Unbounded Memory Consumption]
**Vulnerability:** Unbounded memory consumption DoS risk due to JSON file parsing without size limits in file-backed repositories and stores.
**Learning:** `json.loads(file.read_text())` reads the entire file content into memory. This can lead to out-of-memory errors or denial-of-service if an attacker or misconfiguration provides an excessively large file. The application relies heavily on file-backed adapters (e.g., `JsonFilePracticeRepository`, `JsonFileProgressSnapshotStore`, `CheckpointStore`).
**Prevention:** Implement a strict file size limit check using `path.stat().st_size` (e.g., standardized at 10MB or `10 * 1024 * 1024` bytes) before reading the file content into memory in all file-based adapters.

## 2025-02-23 - [TOCTOU in File Size Check]
**Vulnerability:** Time-of-Check to Time-of-Use (TOCTOU) race condition during file size limit checks.
**Learning:** Checking `path.stat().st_size` before calling `path.read_text()` leaves a gap where an attacker can replace or append to the file, bypassing the limit and causing memory exhaustion DoS. Additionally, special files (like `/dev/zero`) might report 0 size but stream infinite data.
**Prevention:** Instead of checking size via `stat()`, open the file and read with a bounded limit `f.read(limit + 1)`. If the returned string length exceeds the limit, abort parsing. This guarantees the application never reads more than the intended limit into memory.