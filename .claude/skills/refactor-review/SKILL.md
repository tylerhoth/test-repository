---
name: refactor-review
description: Provide a structured refactor plan and safe diffs
invoke: /refactor-review
permissions:
  allow:
    - "pnpm dev"
    - "pnpm test"
    - "pnpm lint"
    - "pnpm fmt"
---

# /refactor-review

Analyze a module or path and produce a structured refactor plan with safe, incremental changes.

## When invoked

1. **Identify target** — The user provides a module path or area to refactor (e.g., `backend/app/services/`, `frontend/src/pages/`).

2. **Analyze** — Read the target files and identify:
   - Code smells (duplication, long functions, tight coupling, etc.)
   - Potential improvements (better abstractions, clearer naming, separation of concerns)
   - Risk areas (changes that could break existing behavior)

3. **Produce refactor plan**:
   ```
   ## Refactor Plan: <target>

   ### Issues Found
   1. <issue description>
   2. <issue description>

   ### Proposed Changes
   1. <change description> — risk: low/medium/high
   2. <change description> — risk: low/medium/high

   ### Order of Operations
   1. <safest change first>
   2. <next change>
   ...
   ```

4. **If the user approves** — Implement changes one at a time:
   - Make one small, focused change
   - Run `pnpm test` to verify nothing broke
   - Commit with a clear message (e.g., `refactor: extract helper for X`)
   - Repeat for each approved change

5. **Final output** — Summary of all changes made, commits created, and test results.
