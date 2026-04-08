## 2025-02-23 - [JSON Parsing Unbounded Memory Consumption]
**Vulnerability:** Unbounded memory consumption DoS risk due to JSON file parsing without size limits in file-backed repositories and stores.
**Learning:** `json.loads(file.read_text())` reads the entire file content into memory. This can lead to out-of-memory errors or denial-of-service if an attacker or misconfiguration provides an excessively large file. The application relies heavily on file-backed adapters (e.g., `JsonFilePracticeRepository`, `JsonFileProgressSnapshotStore`, `CheckpointStore`).
**Prevention:** Implement a strict file size limit check using `path.stat().st_size` (e.g., standardized at 10MB or `10 * 1024 * 1024` bytes) before reading the file content into memory in all file-based adapters.

## 2025-03-23 - [TOCTOU and Device File Size Limit Bypass]
**Vulnerability:** File size checks using `path.stat().st_size` can be bypassed if the path points to a device file (like `/dev/zero`, which reports a size of 0). Additionally, there is a Time-of-Check to Time-of-Use (TOCTOU) vulnerability where a file could be modified between the `stat()` check and the `read_text()` call.
**Learning:** Checking file size before reading is insufficient on its own. Device files bypass `st_size` checks, and files can grow between the size check and the read operation, leading to unbounded memory consumption or application hangs.
**Prevention:** Always verify a path is a regular file first using `path.is_file()`. Then, instead of reading the whole file with `read_text()`, open the file and use a bounded read (e.g., `f.read(limit + 1)`) and check if the returned content length exceeds the limit.
