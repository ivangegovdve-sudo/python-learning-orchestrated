## 2025-02-23 - [JSON Parsing Unbounded Memory Consumption]
**Vulnerability:** Unbounded memory consumption DoS risk due to JSON file parsing without size limits in file-backed repositories and stores.
**Learning:** `json.loads(file.read_text())` reads the entire file content into memory. This can lead to out-of-memory errors or denial-of-service if an attacker or misconfiguration provides an excessively large file. The application relies heavily on file-backed adapters (e.g., `JsonFilePracticeRepository`, `JsonFileProgressSnapshotStore`, `CheckpointStore`).
**Prevention:** Implement a strict file size limit check using `path.stat().st_size` (e.g., standardized at 10MB or `10 * 1024 * 1024` bytes) before reading the file content into memory in all file-based adapters.
## 2025-02-23 - [TOCTOU Vulnerability and OOM DoS in Bounded Reads]
**Vulnerability:** File size limit checks using `path.stat().st_size` combined with `path.read_text()` create TOCTOU (Time-of-Check to Time-of-Use) vulnerabilities and memory DoS risks (e.g., using device files like `/dev/zero` which report size 0 but have infinite stream).
**Learning:** Using `is_file()` to enforce regular files before size checking is critical. Also, using a bounded `read()` (e.g., `content = f.read(limit + 1)`) and verifying the read length prevents unbounded memory consumption safely, without relying on `stat()`.
**Prevention:** Instead of `st_size`, verify `is_file()` first, then use a secure bounded read `content = f.read(10 * 1024 * 1024 + 1)` and raise an error if `len(content) > 10 * 1024 * 1024`.
