---
name: team-kickoff
description: Initialize a new application idea with the full 30-agent engineering team
invoke: /team-kickoff
permissions:
  allow:
    - "pnpm dev"
    - "pnpm test"
    - "pnpm lint"
    - "pnpm fmt"
    - "pnpm gen:types"
---

# /team-kickoff

Bootstrap a new application idea using the multi-agent engineering team.

## When invoked

1. **Gather the idea** — If the user hasn't provided a detailed description, ask for:
   - Application name and purpose
   - Key features (MVP scope)
   - Target users
   - Any technical constraints or preferences

2. **Product spec** — Delegate to `@product-owner` to produce:
   - User stories with acceptance criteria
   - Data model outline
   - API contract sketch
   - MVP vs. future scope

3. **Architecture design** — Delegate to `@solution-architect` to produce:
   - Component diagram
   - Technology decisions (within repo stack: FastAPI + React + TS)
   - Data flow design
   - Integration points

4. **Work breakdown** — Delegate to `@tech-lead` to produce:
   - Phased implementation plan
   - Agent assignments for each task
   - Dependency graph
   - Estimated task ordering

5. **Database design** — Delegate to `@database-architect` to produce:
   - Entity-relationship diagram (text-based)
   - Model definitions
   - Migration plan

6. **API design** — Delegate to `@api-designer` to produce:
   - Full endpoint specifications
   - Request/response schemas
   - Pagination and filtering strategy

7. **Test strategy** — Delegate to `@qa-lead` to produce:
   - Test plan covering all features
   - Backend + frontend test outlines

8. **Output** — Compile all outputs into a structured kickoff document:
   ```
   ## Team Kickoff: <application name>

   ### Product Spec
   <from product-owner>

   ### Architecture
   <from solution-architect>

   ### Work Breakdown
   <from tech-lead>

   ### Database Design
   <from database-architect>

   ### API Design
   <from api-designer>

   ### Test Strategy
   <from qa-lead>

   ### Next Steps
   - Recommended first sprint tasks
   - Which agents to invoke first
   ```
