# ADR-006: Documentation Framework (Scrum Artifacts)

## Date
2026-01-25

## Status
Accepted

## Context
To maintain transparency, traceability, and agile delivery standards, a unified documentation set for Scrum artifacts is required across all development cycles.

## Decision
The following documentation artifacts are mandatory for every project delivery to ensure professional engineering standards and agile transparency:

### 1. Engineering Reports (Legal/Technical Alignment)
- **INCIBE SDS Engineering Report**: A formal document strictly adhering to the INCIBE System Design Specification structure. 
- **Strategic Purpose**: This high-standard specification ensures projects are ready for:
    - Submission to **Cybersecurity R&D+i** project calls.
    - Technical responses for **public and private tenders** (pliegos).
    - Entry into **incubation and acceleration programs**.

### 2. Scrum Artifacts (Agile Traceability)
To comply with the official Scrum framework and C23 standards, every project must maintain and deliver the following artifacts:

#### Core Scrum Artifacts
- **Product Backlog**: The single source of requirements, managed as `[Project]_ProductBacklog.md`.
- **Sprint Backlog**: The set of Product Backlog items selected for the Sprint, plus a plan for delivering the Increment.
- **Increment**: The concrete stepping stone toward the Product Goal (Working source code).

#### C23 Mandatory Deliverable Inventory
The following specific files must be generated and presented as "Ready for Delivery":
- **`[Project]_ProductBacklog.md`**: Fully detailed and prioritized backlog.
- **`[Project]_DefinitionOfDone.md`**: Formal description of the state of the Increment when it meets the quality requirements.
- **`[Project]_ADR-[NNN]-[Category].md`**: A set of Architectural Decision Records, one for each standard category defined in `CONF23-STD-SDLC-001`.

## Consequences
- Reports follow a standardized structure compatible with national (INCIBE) audit requirements.
- Project transparency is maintained through the three pillar Scrum artifacts.
- Compliance and quality checks are explicitly verified against the "Definition of Done".
- Knowledge transfer is facilitated by the categorization of architectural decisions (ADRs).
