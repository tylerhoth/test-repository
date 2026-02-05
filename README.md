# CashLens — Personal Finance Assistant

A personal finance application that ingests transaction data, performs deep analysis, and acts as a professional financial advisor. Built as a monorepo with FastAPI backend and Vite + React + TypeScript frontend.

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
| GET | `/api/accounts` | List accounts |
| POST | `/api/accounts` | Create account |
| GET | `/api/categories` | List categories |
| POST | `/api/categories` | Create category |
| GET | `/api/transactions` | List transactions (filterable by account, category, date range) |
| POST | `/api/transactions` | Create transaction |
| PUT | `/api/transactions/{id}` | Update/recategorize transaction |
| DELETE | `/api/transactions/{id}` | Delete transaction |
| POST | `/api/transactions/import` | Import CSV file |
| GET | `/api/category-rules` | List auto-categorization rules |
| POST | `/api/category-rules` | Create categorization rule |
| GET | `/api/budgets` | List budgets |
| POST | `/api/budgets` | Create/update budget |
| DELETE | `/api/budgets/{id}` | Delete budget |
| GET | `/api/dashboard/summary` | Financial summary (income, expenses, savings rate) |
| GET | `/api/dashboard/spending-by-category` | Category spending breakdown |
| GET | `/api/dashboard/income-vs-expenses` | Monthly income vs expenses |
| GET | `/api/dashboard/recurring` | Detected recurring charges |
| GET | `/api/insights` | Financial insights |
| GET | `/api/labels` | List labels |
| POST | `/api/labels` | Create label |
| DELETE | `/api/labels/{id}` | Delete label |
| GET | `/api/todos` | List todos |
| POST | `/api/todos` | Create todo |
| DELETE | `/api/todos/{id}` | Delete todo |

### List endpoint query params

- `page` (default: 1)
- `page_size` (default: 20, max: 100)
- `q` — search filter
- `sort_by` — field to sort by (allowlist per entity)
- `sort_dir` — `asc` or `desc`
- `account_id` — filter transactions by account
- `category_id` — filter transactions by category
- `date_from` / `date_to` — filter transactions by date range

Response shape: `{ items, total, page, page_size }`

### CSV Import Format

The import endpoint accepts CSV files with columns: `Date, Description, Category, Firm Name, Account Name, Amount, Tags`. Accounts and categories are auto-created on import. Sample data is in `backend/data/sample_transactions.csv`.

## Multi-Agent Engineering Team

This repo includes a **30-agent AI engineering team** in `.claude/agents/`. Claude Code automatically delegates to the right specialist based on task context. You can also invoke agents explicitly.

### Team Structure

| Group | Agents | Roles |
|-------|--------|-------|
| Leadership (3) | tech-lead, product-owner, scrum-master | Coordination, specs, progress tracking |
| Architecture (3) | solution-architect, api-designer, database-architect | System design, API contracts, schema design |
| Backend (4) | backend-senior, backend-api, backend-services, backend-data | Full-stack backend implementation |
| Frontend (4) | frontend-senior, frontend-components, frontend-pages, frontend-state | React components, pages, state management |
| Quality (4) | qa-lead, test-backend, test-frontend, test-e2e | Test strategy, test writing, E2E scenarios |
| DevOps (3) | devops-engineer, infra-architect, site-reliability | CI/CD, infrastructure, monitoring |
| Security (2) | security-auditor, security-reviewer | Vulnerability audit, security code review |
| Code Quality (3) | code-reviewer, refactor-specialist, performance-engineer | Review, refactoring, optimization |
| Specialized (4) | debugger, technical-writer, knowledge-curator, integration-specialist | Debugging, docs, knowledge, integrations |
| Creative (1) | idea-generator | Brainstorm and evaluate app ideas |

### Usage

```
# Direct delegation
Use the backend-senior agent to implement a Comments feature
Have the security-auditor scan the codebase

# Orchestrated workflows (skills)
/team-kickoff    — Bootstrap a new app idea with the full team
/build-app       — Implement a feature end-to-end with all agents
/sprint-plan     — Plan and execute a sprint of coordinated work
/team-review     — Multi-agent code + security + performance review
```

## Claude Code Skills

This repo includes Claude Code skills in `.claude/skills/`:

| Skill | Description |
|-------|-------------|
| `/team-kickoff` | Bootstrap a new app idea with the full agent team |
| `/build-app` | End-to-end implementation from idea to working code |
| `/sprint-plan` | Plan and execute a sprint across multiple agents |
| `/team-review` | Multi-agent code, security, and performance review |
| `/feature-slice` | Generate a full-stack CRUD feature for a new entity |
| `/test-triage` | Run tests and diagnose failures |
| `/deploy-prep` | Add Dockerfiles, CI, and deployment checklist |
| `/refactor-review` | Analyze code and produce a safe refactor plan |
