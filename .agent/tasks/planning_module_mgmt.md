---
name: project-planner
description: Plan the "Tenant Module Management" feature.
---

# User Request
"Implement the modules on the UI... system admins might be able to enable/disable modules/mfes and also select which version the tenants use. The tenants should have some way to identify version of the module and name so they could open tickets later properly."

# Context
*   **Architecture**: Microservices (`programs`, `rules`, `ingestion`, `claims`, `gateway`).
*   **Frontend**: Next.js Monorepo (Shell + MFEs).
*   **Current State**: `services/programs` owns Tenant Configuration.

# Goal
Create a plan (`module-management.md`) to:
1.  **Backend**: Add `ModuleConfig` table to `services/programs`.
    *   Fields: `tenant_id`, `module_name` (e.g. 'offers', 'loyalty'), `is_enabled`, `version` (string).
    *   API: `GET/PUT /admin/tenants/{id}/modules`.
2.  **Frontend (Admin)**:
    *   Create "Module Management" view in Admin Dashboard.
    *   UI: List of modules, Toggle Switch (Enable/Disable), Input/Dropdown (Version).
    *   Style: Follow "Technical Brutalism" (Emerald/Slate, No Purple).
3.  **Frontend (Shell)**:
    *   Update `MFERegistry` or Navigation to check `is_enabled` before showing links.
    *   Display "Version" in the User Profile/Help menu for the tenant.

# Deliverable
*   `module-management.md` plan file.
