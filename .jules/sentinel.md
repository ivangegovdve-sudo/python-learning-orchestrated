## 2025-02-23 - [JSON Parsing Unbounded Memory Consumption]
**Vulnerability:** Unbounded memory consumption DoS risk due to JSON file parsing without size limits in file-backed repositories and stores.
**Learning:** `json.loads(file.read_text())` reads the entire file content into memory. This can lead to out-of-memory errors or denial-of-service if an attacker or misconfiguration provides an excessively large file. The application relies heavily on file-backed adapters (e.g., `JsonFilePracticeRepository`, `JsonFileProgressSnapshotStore`, `CheckpointStore`).
**Prevention:** Implement a strict file size limit check using `path.stat().st_size` (e.g., standardized at 10MB or `10 * 1024 * 1024` bytes) before reading the file content into memory in all file-based adapters.
## 2024-03-20 - Unbounded File Read in JsonFilePracticeRepository
 **Vulnerability:** Unbounded file read into memory and potential DoS via device files (like `/dev/zero`).
 **Learning:** Relying solely on `st_size` checks before reading a file is insufficient. Special files might report zero size but generate endless output. Furthermore, an attacker might swap the file between the `stat()` check and the `read()` call (TOCTOU).
 **Prevention:** Verify `is_file()` to reject device files and always enforce a hard limit on the `read()` buffer (e.g., `f.read(limit + 1)`) to detect and abort oversized reads.
