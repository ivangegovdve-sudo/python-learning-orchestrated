## 2024-05-24 - [Batch DB operations in progress importer]
**Learning:** Repetitive I/O operations (like file reads and writes) in a loop, particularly when importing large payloads like progress snapshots, result in huge performance bottlenecks (O(N^2)). The cost stems from repeatedly deserializing/serializing and accessing the filesystem instead of modifying the state in memory first.
**Action:** When saving many records from an import or mass update, always use or introduce batched methods (e.g. `save_items` vs `save_item`) to perform the filesystem or DB I/O once.
