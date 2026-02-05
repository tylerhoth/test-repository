---
name: test-triage
description: Run tests and diagnose failures
invoke: /test-triage
permissions:
  allow:
    - "pnpm dev"
    - "pnpm test"
    - "pnpm lint"
    - "pnpm fmt"
---

# /test-triage

Run the full test suite and diagnose any failures.

## When invoked

1. **Run tests** — Execute `pnpm test` to run both backend and frontend test suites.

2. **Parse output** — Identify:
   - Failing test suite(s) and file path(s)
   - Failing test name(s)
   - Error messages and stack traces

3. **Produce triage report** with this structure:
   ```
   ## Test Triage Report

   ### Failing Suites
   - <suite file path>

   ### Failing Tests
   - <test name> — <short error summary>

   ### Likely Root Cause
   <analysis of what is most likely causing the failure>

   ### Minimal Fix Plan
   1. <step 1>
   2. <step 2>
   ...
   ```

4. **If the user allows fixes** — Implement the minimal fix plan:
   - Make the smallest change that fixes the failing tests
   - Run `pnpm test` again to confirm all tests pass
   - If tests still fail, iterate (up to 3 attempts) or report that manual intervention is needed

5. **Final output** — Report whether all tests now pass or what remains broken.
