# Fullstack Starter

A monorepo with a FastAPI backend and a Vite + React + TypeScript frontend.

## Prerequisites

- Python 3.11+
- Node.js 20+
- pnpm 10+

## Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
python3 -m alembic upgrade head
```

### Frontend

```bash
pnpm install   # from repo root — installs root + frontend deps
```

## Commands

All commands run from the repo root:

| Command | Description |
|---------|-------------|
| `pnpm dev` | Run backend (port 8000) + frontend (port 5173) concurrently |
| `pnpm test` | Run backend (pytest) + frontend (vitest) tests |
| `pnpm lint` | Lint backend (ruff) + frontend (eslint) |
| `pnpm fmt` | Format backend (ruff) + frontend (prettier) |
| `pnpm gen:types` | Generate TypeScript types from backend OpenAPI spec |

## Architecture

### Backend (`backend/`)

Layered FastAPI application:

- `app/api/` — route handlers
- `app/services/` — business logic
- `app/repositories/` — data access
- `app/schemas/` — Pydantic request/response schemas
- `app/models/` — SQLAlchemy ORM models
- `app/db/` — database engine and session
- `app/tests/` — pytest test suite

Database: SQLite (local dev) via SQLAlchemy 2.0 with Alembic migrations.

### Frontend (`frontend/`)

Vite + React + TypeScript SPA:

- `src/api/` — API client and generated OpenAPI types
- `src/pages/` — page components
- `src/tests/` — vitest test suite

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/version` | App version |
| GET | `/api/todos` | List todos (paginated, searchable, sortable) |
| POST | `/api/todos` | Create a todo |
| DELETE | `/api/todos/{id}` | Delete a todo |

### List endpoint query params

- `page` (default: 1)
- `page_size` (default: 20, max: 100)
- `q` — search filter on title
- `sort_by` — field to sort by (allowlist: id, title, completed, created_at)
- `sort_dir` — `asc` or `desc`

Response shape: `{ items, total, page, page_size }`

## Claude Code Skills

This repo includes Claude Code skills in `.claude/skills/`:

| Skill | Description |
|-------|-------------|
| `/feature-slice` | Generate a full-stack CRUD feature for a new entity |
| `/test-triage` | Run tests and diagnose failures |
| `/deploy-prep` | Add Dockerfiles, CI, and deployment checklist |
| `/refactor-review` | Analyze code and produce a safe refactor plan |
