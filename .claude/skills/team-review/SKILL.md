---
name: team-review
description: Coordinate a multi-agent review of recent changes including code, security, and performance
invoke: /team-review
permissions:
  allow:
    - "pnpm dev"
    - "pnpm test"
    - "pnpm lint"
    - "pnpm fmt"
---

# /team-review

Run a comprehensive multi-agent review of recent changes.

## When invoked

1. **Identify changes** — Run `git diff` and `git log` to identify what's changed since the last review.

2. **Parallel reviews** — Delegate to multiple reviewers simultaneously:

   - `@code-reviewer` — Code quality, readability, standards compliance
   - `@security-reviewer` — Security implications of the changes
   - `@performance-engineer` — Performance impact assessment
   - `@qa-lead` — Test coverage assessment

3. **Compile report**:

   ```
   ## Team Review Report

   ### Changes Reviewed
   - <list of files changed>
   - <summary of what changed>

   ### Code Review (@code-reviewer)
   <findings>

   ### Security Review (@security-reviewer)
   <findings>

   ### Performance Review (@performance-engineer)
   <findings>

   ### Test Coverage (@qa-lead)
   <findings>

   ### Consolidated Action Items
   | Priority | Issue | Reviewer | File | Action |
   |----------|-------|----------|------|--------|

   ### Overall Verdict
   APPROVE / REQUEST CHANGES / NEEDS DISCUSSION
   ```

4. **If fixes needed** — Delegate fixes to the appropriate agent:
   - Security issues → `@security-auditor` + `@backend-senior` or `@frontend-senior`
   - Performance issues → `@performance-engineer`
   - Test gaps → `@test-backend` or `@test-frontend`
   - Code quality → `@refactor-specialist`

5. **Re-verify** — After fixes, run `pnpm test` and `pnpm lint` to confirm everything passes.
