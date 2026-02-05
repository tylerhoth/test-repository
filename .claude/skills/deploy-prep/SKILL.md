---
name: deploy-prep
description: Prepare deployment scaffolding without locking to a provider
invoke: /deploy-prep
permissions:
  allow:
    - "pnpm dev"
    - "pnpm test"
    - "pnpm lint"
    - "pnpm fmt"
---

# /deploy-prep

Prepare deployment scaffolding without choosing a specific hosting provider.

## When invoked

1. **Backend Dockerfile** — Create `backend/Dockerfile`:
   - Python base image
   - Install deps from `requirements.txt`
   - Copy app code
   - Expose port 8000
   - Run with `uvicorn app.main:app --host 0.0.0.0 --port 8000`

2. **Frontend Dockerfile** — Create `frontend/Dockerfile`:
   - Node base image for build stage
   - Install deps with `pnpm install --frozen-lockfile`
   - Build with `pnpm build`
   - Nginx (or similar) stage to serve static files

3. **CI workflow** — Create `.github/workflows/ci.yml`:
   - Trigger on push and pull request
   - Steps:
     - Checkout code
     - Set up Python and Node
     - Install dependencies
     - Run `pnpm lint`
     - Run `pnpm test`

4. **Deployment checklist** — Create `docs/deploy/CHECKLIST.md`:
   - Provider-agnostic deployment steps
   - Environment variables to set
   - Database migration steps
   - Health check verification
   - Rollback procedure

5. **Run tests** — Execute `pnpm test` to ensure nothing was broken.

6. **Summary** — Output list of files created and next steps for the user.
