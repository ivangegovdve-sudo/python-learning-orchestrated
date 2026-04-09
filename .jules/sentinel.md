## 2025-02-23 - [JSON Parsing Unbounded Memory Consumption]
**Vulnerability:** Unbounded memory consumption DoS risk due to JSON file parsing without size limits in file-backed repositories and stores.
**Learning:** `json.loads(file.read_text())` reads the entire file content into memory. This can lead to out-of-memory errors or denial-of-service if an attacker or misconfiguration provides an excessively large file. The application relies heavily on file-backed adapters (e.g., `JsonFilePracticeRepository`, `JsonFileProgressSnapshotStore`, `CheckpointStore`).
**Prevention:** Implement a strict file size limit check using `path.stat().st_size` (e.g., standardized at 10MB or `10 * 1024 * 1024` bytes) before reading the file content into memory in all file-based adapters.
## 2024-05-09 - Prevent Unbounded File Read DoS
 **Vulnerability:** Unbounded file read into memory allowing OOM DoS
 **Learning:** Relying on `os.stat().st_size` for size limits is insufficient because it is susceptible to TOCTOU vulnerabilities and can be bypassed with device files like `/dev/zero` which report size 0 but produce infinite output.
 **Prevention:** Use `is_file()` to ensure the target is a regular file before reading, and employ a bounded read strategy (e.g. `f.read(limit + 1)`) checking if the returned content length exceeds the intended limit to mitigate both issues.
