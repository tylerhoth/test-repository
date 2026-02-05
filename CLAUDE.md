# Fullstack Starter — Project Instructions

## Stack

- **Backend**: FastAPI + SQLAlchemy 2.0 + SQLite + Alembic (Python 3.11+)
- **Frontend**: Vite + React + TypeScript + Vitest (Node 20+, pnpm)
- **Monorepo**: pnpm workspace with root-level orchestration scripts

## Commands

All from repo root:

| Command | What it does |
|---------|-------------|
| `pnpm dev` | Backend (8000) + Frontend (5173) concurrently |
| `pnpm test` | pytest + vitest |
| `pnpm lint` | ruff + eslint |
| `pnpm fmt` | ruff format + prettier |
| `pnpm gen:types` | Export OpenAPI spec → TypeScript types |

## Architecture

```
backend/app/
  api/         → FastAPI routers (endpoints)
  services/    → Business logic
  repositories/→ Data access (SQLAlchemy)
  schemas/     → Pydantic models
  models/      → SQLAlchemy ORM
  db/          → Engine/session
  tests/       → pytest

frontend/src/
  api/         → Fetch client + generated types
  pages/       → Page components
  components/  → Reusable UI
  tests/       → vitest
```

## Conventions

- List endpoints: `page`, `page_size`, `q`, `sort_by`, `sort_dir`
- Response envelope: `{ items, total, page, page_size }`
- Sorting: allowlist-based (SORTABLE_FIELDS set)
- Primary keys: integer autoincrement `id`
- Create → 201, Delete → 204, Not found → 404

## Agent Team (30 engineers)

This repo includes a 30-agent engineering team in `.claude/agents/`. Claude automatically delegates to the right specialist based on task context.

### Team Roster

**Leadership**
| Agent | Role | Model |
|-------|------|-------|
| tech-lead | Task decomposition, agent coordination | opus |
| product-owner | Requirements → specs | opus |
| scrum-master | Progress tracking, blockers | haiku |

**Architecture**
| Agent | Role | Model |
|-------|------|-------|
| solution-architect | System design, trade-offs | opus |
| api-designer | REST API contracts | sonnet |
| database-architect | Schema design, migrations | sonnet |

**Backend**
| Agent | Role | Model |
|-------|------|-------|
| backend-senior | Full-stack backend features | sonnet |
| backend-api | FastAPI route handlers | sonnet |
| backend-services | Business logic layer | sonnet |
| backend-data | Repository / data access | sonnet |

**Frontend**
| Agent | Role | Model |
|-------|------|-------|
| frontend-senior | Full-stack frontend features | sonnet |
| frontend-components | Reusable React components | sonnet |
| frontend-pages | Page composition | sonnet |
| frontend-state | State management, API integration | sonnet |

**Quality & Testing**
| Agent | Role | Model |
|-------|------|-------|
| qa-lead | Test strategy, coverage planning | sonnet |
| test-backend | pytest test writing | sonnet |
| test-frontend | vitest test writing | sonnet |
| test-e2e | End-to-end scenarios | sonnet |

**DevOps & Infrastructure**
| Agent | Role | Model |
|-------|------|-------|
| devops-engineer | CI/CD, Docker, deployment | sonnet |
| infra-architect | Cloud infra design | sonnet |
| site-reliability | Monitoring, reliability | sonnet |

**Security**
| Agent | Role | Model |
|-------|------|-------|
| security-auditor | Vulnerability audit (OWASP) | sonnet |
| security-reviewer | Security-focused code review | sonnet |

**Code Quality**
| Agent | Role | Model |
|-------|------|-------|
| code-reviewer | Code review, standards | sonnet |
| refactor-specialist | Safe incremental refactoring | sonnet |
| performance-engineer | Profiling, optimization | sonnet |

**Specialized**
| Agent | Role | Model |
|-------|------|-------|
| debugger | Root cause analysis, bug fixing | sonnet |
| technical-writer | Documentation | haiku |
| knowledge-curator | ADRs, patterns, conventions | haiku |
| integration-specialist | External API connections | sonnet |
| idea-generator | Brainstorm and evaluate app ideas | opus |

### Orchestration Skills

| Skill | Purpose |
|-------|---------|
| `/team-kickoff` | Bootstrap a new app idea with the full team |
| `/sprint-plan` | Plan and execute a sprint of work |
| `/team-review` | Multi-agent code + security + performance review |
| `/build-app` | End-to-end: idea → working code |
| `/feature-slice` | Generate a full-stack CRUD feature |
| `/test-triage` | Diagnose and fix test failures |
| `/deploy-prep` | Dockerfiles, CI, deployment checklist |
| `/refactor-review` | Structured refactor with safe diffs |

### How to Use the Team

**Direct delegation:**
```
Use the backend-senior agent to implement a new Comments feature
Have the security-auditor scan the codebase
Use the debugger to fix the failing test in test_todos.py
```

**Orchestrated workflows:**
```
/team-kickoff — to start a new application idea
/build-app — to implement a feature end-to-end
/sprint-plan — to plan and execute a batch of work
/team-review — to get a comprehensive review
```

**Parallel work:**
```
Run code-reviewer and security-reviewer in parallel on the latest changes
Have test-backend and test-frontend write tests simultaneously
```
