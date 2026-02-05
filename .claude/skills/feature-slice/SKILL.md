---
name: feature-slice
description: Generate a full-stack "enterprise CRUD" slice for a new entity
invoke: /feature-slice
permissions:
  allow:
    - "pnpm dev"
    - "pnpm test"
    - "pnpm lint"
    - "pnpm fmt"
    - "pnpm gen:types"
---

# /feature-slice

Generate a complete full-stack CRUD feature slice for a new entity.

## When invoked

1. **Gather entity spec** — If the user did not provide an entity spec, ask for:
   - Entity name (singular, PascalCase)
   - Fields: name, type, nullable, default
   - Which fields are searchable (used in `q` filter)
   - Which fields are sortable (added to the sort allowlist)

2. **Backend generation** — Create the following under `backend/app/`:
   - `models/<entity>.py` — SQLAlchemy model with integer autoincrement `id` as PK
   - `schemas/<entity>.py` — Pydantic schemas: `<Entity>Create`, `<Entity>Out`, `<Entity>ListResponse`
   - `repositories/<entity>.py` — Repository with `list` (page/page_size/q/sort_by/sort_dir), `create`, `get_by_id`, `delete`. Sorting is **allowlist-based**.
   - `services/<entity>.py` — Service layer calling the repository
   - `api/<entity_plural>.py` — FastAPI router with:
     - `GET /api/<entity_plural>` — enterprise list with `page`, `page_size`, `q`, `sort_by`, `sort_dir`; response envelope `{ items, total, page, page_size }`
     - `POST /api/<entity_plural>`
     - `DELETE /api/<entity_plural>/{id}`
   - Register the router in `app/main.py`
   - Update `app/models/__init__.py` to import the new model

3. **Alembic migration** — Generate with:
   ```
   cd backend && python3 -m alembic revision --autogenerate -m "create <entity_plural> table"
   ```
   Verify the migration has both `upgrade()` and `downgrade()`.

4. **Backend tests** — Create `app/tests/test_<entity_plural>.py` with tests for:
   - Create, list (empty + with items), pagination, search, sort, delete, delete-not-found

5. **Frontend generation** — Create under `frontend/src/`:
   - `api/<entity_plural>.ts` — typed client functions using the fetch wrapper
   - `pages/<Entity>Page.tsx` — React page with list, create form, and delete
   - `tests/<Entity>Page.test.tsx` — Vitest tests with mocked API

6. **OpenAPI types** — Run `pnpm gen:types` to regenerate TypeScript types from the updated backend.

7. **Format & Test**:
   - Run `pnpm fmt`
   - Run `pnpm test`

8. **Git**:
   - Create branch `feature/<entity>-slice`
   - Commit with message `feat: add <entity> feature slice`

9. **Summary** — Output:
   - Files created/changed
   - Commands run
   - Test results
