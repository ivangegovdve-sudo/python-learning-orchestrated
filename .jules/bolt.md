## 2024-05-24 - [Batch DB operations in progress importer]
**Learning:** Repetitive I/O operations (like file reads and writes) in a loop, particularly when importing large payloads like progress snapshots, result in huge performance bottlenecks (O(N^2)). The cost stems from repeatedly deserializing/serializing and accessing the filesystem instead of modifying the state in memory first.
**Action:** When saving many records from an import or mass update, always use or introduce batched methods (e.g. `save_items` vs `save_item`) to perform the filesystem or DB I/O once.

## 2024-03-14 - Redundant Disk I/O on Idempotent Import
**Learning:** During progress import (`ImportProgress.run`), checking equality before calling `repository.save_item()` significantly speeds up processing when most items are unchanged (idempotent imports). In JSON file-backed adapters, each `save_item` forces a full disk dump/sync, turning O(N) unchanged merges into extremely slow O(N) file rewrites.
**Action:** Always check if a domain item actually mutated before persisting it in iterative loops. Fetch related data once per operation instead of inside loops or repeatedly.
