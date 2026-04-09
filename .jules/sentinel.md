## 2025-02-23 - [JSON Parsing Unbounded Memory Consumption]
**Vulnerability:** Unbounded memory consumption DoS risk due to JSON file parsing without size limits in file-backed repositories and stores.
**Learning:** `json.loads(file.read_text())` reads the entire file content into memory. This can lead to out-of-memory errors or denial-of-service if an attacker or misconfiguration provides an excessively large file. The application relies heavily on file-backed adapters (e.g., `JsonFilePracticeRepository`, `JsonFileProgressSnapshotStore`, `CheckpointStore`).
**Prevention:** Implement a strict file size limit check using `path.stat().st_size` (e.g., standardized at 10MB or `10 * 1024 * 1024` bytes) before reading the file content into memory in all file-based adapters.

## 2025-02-23 - [TOCTOU and Device File DoS in File Size Checks]
**Vulnerability:** Denial of Service (DoS) and Time-of-Check to Time-of-Use (TOCTOU) race condition when validating file sizes.
**Learning:** Relying on `path.stat().st_size` before reading a file is insecure for two reasons: 1) A file's contents can be changed between the size check and the read operation (TOCTOU). 2) Device files like `/dev/zero` report a size of 0 via `stat()` but produce infinite output when read, bypassing the size limit and causing an Out-of-Memory (OOM) crash if read entirely using `.read_text()`.
**Prevention:** Always verify a path is a regular file using `path.is_file()` to reject device files. Additionally, use a bounded read pattern (e.g., `content = f.read(limit + 1)`) and check the length of the read content instead of relying on `stat().st_size` to prevent TOCTOU bypasses.
