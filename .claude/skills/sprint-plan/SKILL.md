---
name: sprint-plan
description: Plan and execute a sprint of work across multiple agents
invoke: /sprint-plan
permissions:
  allow:
    - "pnpm dev"
    - "pnpm test"
    - "pnpm lint"
    - "pnpm fmt"
    - "pnpm gen:types"
---

# /sprint-plan

Plan a sprint of work and coordinate agent execution.

## When invoked

1. **Gather scope** — Ask the user what features or tasks to include in this sprint.

2. **Status check** — Delegate to `@scrum-master`:
   - Run `pnpm test` to check current health
   - Check `git log` for recent work
   - Identify any blockers or incomplete work

3. **Decompose work** — Delegate to `@tech-lead`:
   - Break features into implementable tasks
   - Assign each task to a specific agent
   - Order by dependencies (what can run in parallel)
   - Group into phases

4. **Produce sprint plan**:

   ```
   ## Sprint Plan

   ### Goal
   <what this sprint delivers>

   ### Current State
   - Tests: <status>
   - Last commits: <recent work>

   ### Phase 1: <name> (parallel tasks)
   | Task | Agent | Dependencies | Description |
   |------|-------|-------------|-------------|

   ### Phase 2: <name> (after Phase 1)
   | Task | Agent | Dependencies | Description |
   |------|-------|-------------|-------------|

   ### Quality Gate (after all phases)
   - [ ] `pnpm test` — all passing
   - [ ] `pnpm lint` — clean
   - [ ] `@code-reviewer` — review all changes
   - [ ] `@security-reviewer` — security review

   ### Definition of Done
   - All tasks completed
   - All tests passing
   - Code reviewed
   - Docs updated
   ```

5. **Execute** — If the user approves, begin executing:
   - Work through phases in order
   - Delegate each task to the assigned agent
   - Run quality gates between phases
   - Report progress after each phase

6. **Retrospective** — After sprint completion:
   - Delegate to `@scrum-master` for summary
   - List what was completed, what was deferred
   - Recommend next sprint priorities
