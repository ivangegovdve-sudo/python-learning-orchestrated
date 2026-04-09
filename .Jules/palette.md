## 2024-05-18 - Visual Progress Bars in CLI Apps
**Learning:** Adding visual text progress bars (e.g., `[█████░░░░░]`) to CLI applications provides a better micro-interaction and sense of accomplishment compared to purely numeric states (e.g., "1/2"). It makes the interface feel more polished and visually rewarding.
**Action:** Always look for opportunities to replace or augment purely numeric progress indicators with visual text-based representations in CLI tools to improve the user experience.

## 2024-05-24 - CLI Output Scannability and Human-Readability
**Learning:** In text-based CLI menus, using internal identifiers (like `lesson-1`) and verbose status strings (like `pending` or `completed`) makes lists hard to scan and feels too technical.
**Action:** When displaying lists of items with states, use familiar visual symbols (like `[x]` vs `[ ]`) and human-readable titles (like "Variables") to improve scannability and create a more friendly, intuitive interface.

## 2024-05-25 - Actionable Empty States
**Learning:** When users encounter an empty state in a CLI application (e.g., listing resources that don't exist yet), showing only a "None found" message leaves them stranded and degrades the UX. They have to guess or look up the command to create the resource.
**Action:** Always pair empty state messages with a clear, actionable instruction or command on how to create the missing resource (e.g., "No checkpoints found. Use 'checkpoint create <name>' to save one.").
