## 2025-02-23 - [JSON Parsing Unbounded Memory Consumption]
**Vulnerability:** Unbounded memory consumption DoS risk due to JSON file parsing without size limits in file-backed repositories and stores.
**Learning:** `json.loads(file.read_text())` reads the entire file content into memory. This can lead to out-of-memory errors or denial-of-service if an attacker or misconfiguration provides an excessively large file. The application relies heavily on file-backed adapters (e.g., `JsonFilePracticeRepository`, `JsonFileProgressSnapshotStore`, `CheckpointStore`).
**Prevention:** Implement a strict file size limit check using `path.stat().st_size` (e.g., standardized at 10MB or `10 * 1024 * 1024` bytes) before reading the file content into memory in all file-based adapters.
## 2025-02-23 - [File Read Bypass and Unbounded Memory]
**Vulnerability:** Checking file sizes with `path.stat().st_size` allows an attacker to supply a device file (like `/dev/zero`) that reports `0` size, bypassing the check, leading to unbounded memory consumption when reading the file.
**Learning:** `path.is_file()` must always be checked alongside a bounded read (e.g. `f.read(limit)`) instead of `path.read_text()` or `path.stat().st_size`, preventing TOCTOU attacks and device file infinite streams.
**Prevention:** Implement `if not path.is_file(): return {}` and `content = f.read(10 * 1024 * 1024 + 1)` before parsing files.
