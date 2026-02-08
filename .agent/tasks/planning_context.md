---
name: project-planner
description: Architect and Plan the Microservices Split and Ingestion Engine
---

# Context
The user wants to pivot from a Monolithic "Offers" service to a Microservices Architecture:
1.  `services/programs`: Manage Programs, Products, Tenants (Config).
2.  `services/rules`: Stateless Logic Engine (Validation).
3.  `services/ingestion`: **NEW**. Async processing of Sales Logs (CSV/API) -> Claims.

# Goal
Rewrite `implementation_plan.md` to reflect this new architecture.

# Key Decisions (from Discovery)
1.  **Ingestion Pipeline**:
    *   Raw Log -> Normalization -> Rule Matching -> Claim Creation.
2.  **Data Flow**:
    *   `Ingestion` owns `SalesLog`.
    *   `Programs` owns `IncentiveProgram`, `Product`.
    *   `Rules` owns `RuleDefinition`.
    *   `Claims` (legacy/core) owns the final `Claim` entity.
3.  **Tech Stack**: Python/FastAPI + Temporal (Workflows) + PostgreSQL (Split Schemas).

# Requirements
1.  Create a strict **Migration Plan** (Splitting `services/offers`).
2.  Define the **Ingestion API** (`POST /ingest/sales-log`).
3.  Define the **Attribution Workflow** (Temporal).
