# ADR-001: Project Categorization

## Date
2026-01-25

## Status
Accepted

## Context
The C23 Software Factory handles a variety of projects ranging from simple scripts to complex LLM orchestrations. We need a standardized way to categorize these projects to apply the appropriate security context and architectural patterns.

## Decision
We will categorize all projects into one of the following four strictly defined categories:
- **SCRIPT**: CLI tasks and ephemeral execution.
- **TOOL**: Standalone desktop applications.
- **WEB_APP/SAAS**: Distributed cloud architectures (OWASP Top 10 2025 context).
- **LLM_CORE**: Custom LLM training, Fine-tuning, or RAG-Orchestration systems (OWASP Top 10 LLM 2025 context).

## Consequences
- Every project must identify its category at initiation.
- The choice of category dictates the applicable security baseline (e.g., OWASP Top 10 vs. OWASP LLM Top 10).
- Architectural reviews will be tailored to the specific category risks.
