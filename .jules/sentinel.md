## 2025-02-23 - [JSON Parsing Unbounded Memory Consumption]
**Vulnerability:** Unbounded memory consumption DoS risk due to JSON file parsing without size limits in file-backed repositories and stores.
**Learning:** `json.loads(file.read_text())` reads the entire file content into memory. This can lead to out-of-memory errors or denial-of-service if an attacker or misconfiguration provides an excessively large file. The application relies heavily on file-backed adapters (e.g., `JsonFilePracticeRepository`, `JsonFileProgressSnapshotStore`, `CheckpointStore`).
**Prevention:** Implement a strict file size limit check using `path.stat().st_size` (e.g., standardized at 10MB or `10 * 1024 * 1024` bytes) before reading the file content into memory in all file-based adapters.
## 2025-02-23 - [Device File Unbounded Memory DoS Bypass]
**Vulnerability:** A local attacker could bypass the 10MB file size limit check by supplying a device file (e.g., `/dev/zero`) as input, causing `path.stat().st_size` to return `0`. This bypasses the size check and causes `read_text()` to read an infinite stream of zeros, leading to unbounded memory consumption and a Denial of Service (DoS) crash.
**Learning:** `path.stat().st_size` returns `0` for character device files like `/dev/zero` or `/dev/urandom`. Solely relying on `st_size` for size limiting is insufficient if the file type is not validated first.
**Prevention:** Always check if the file is a regular file using `path.is_file()` before relying on `st_size` to enforce size limits when reading files into memory.
