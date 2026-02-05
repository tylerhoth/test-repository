---
name: build-app
description: End-to-end application building — takes an idea from concept to working code using the full agent team
invoke: /build-app
permissions:
  allow:
    - "pnpm dev"
    - "pnpm test"
    - "pnpm lint"
    - "pnpm fmt"
    - "pnpm gen:types"
---

# /build-app

Build a complete application feature or idea from concept to working code.

## When invoked

1. **Kickoff** — If no spec exists, run `/team-kickoff` first to generate one.

2. **Implementation order**:

   ### Phase 1: Backend Foundation
   - `@database-architect` — Create models and migrations
   - `@backend-data` — Implement repositories
   - `@backend-services` — Implement service layer
   - `@backend-api` — Implement API endpoints
   - `@test-backend` — Write backend tests
   - Verify: `pnpm test` (backend only)

   ### Phase 2: Type Bridge
   - Run `pnpm gen:types` to generate frontend TypeScript types

   ### Phase 3: Frontend
   - `@frontend-state` — Create API client modules
   - `@frontend-pages` — Build page components
   - `@frontend-components` — Build reusable components (if needed)
   - `@test-frontend` — Write frontend tests
   - Verify: `pnpm test` (full suite)

   ### Phase 4: Quality
   - `@code-reviewer` — Review all changes
   - `@security-reviewer` — Security review
   - Run `pnpm lint` and `pnpm fmt`

3. **Verification**:
   - `pnpm test` — all tests pass
   - `pnpm lint` — no lint errors
   - `pnpm fmt` — code formatted

4. **Summary** — Output:
   - Files created/modified
   - Endpoints added
   - Test count (backend + frontend)
   - Any follow-up work needed
