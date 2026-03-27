## 2024-05-18 - Visual Progress Bars in CLI Apps
**Learning:** Adding visual text progress bars (e.g., `[█████░░░░░]`) to CLI applications provides a better micro-interaction and sense of accomplishment compared to purely numeric states (e.g., "1/2"). It makes the interface feel more polished and visually rewarding.
**Action:** Always look for opportunities to replace or augment purely numeric progress indicators with visual text-based representations in CLI tools to improve the user experience.

## 2024-05-24 - CLI Output Scannability and Human-Readability
**Learning:** In text-based CLI menus, using internal identifiers (like `lesson-1`) and verbose status strings (like `pending` or `completed`) makes lists hard to scan and feels too technical.
**Action:** When displaying lists of items with states, use familiar visual symbols (like `[x]` vs `[ ]`) and human-readable titles (like "Variables") to improve scannability and create a more friendly, intuitive interface.

## 2024-05-25 - Actionable Empty States in CLI
**Learning:** Showing a generic "No [items] found" message in a CLI leaves the user at a dead-end, unsure of what to do next. Providing actionable instructions directly in the empty state helps guide them to the right command.
**Action:** Always pair empty state messages with clear, actionable instructions or commands on how to create the missing resource to improve the user experience and avoid dead-ends.
