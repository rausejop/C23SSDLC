# ADR-004: Execution Workflow

## Date
2026-01-25

## Status
Accepted

## Context
To maximize efficiency and quality within the C23 Software Factory, a standardized development workflow integrated with Google Antigravity is necessary.

## Decision
The development process will follow a strict "Mental Sandbox" workflow:
1. **Antigravity Optimization**: Optimize prompts for Gemini Flash 3 and structured for side-by-side editing.
2. **Category Analysis**: Immediate identification of SCRIPT, TOOL, WEB_APP, or LLM_CORE.
3. **SOLID Architecture**: Mandatory use of DRY and SOLID principles.
4. **Automated Verification**: Syntax and logic verification prior to artifact generation.
5. **Artifact Generation**: Mandatory generation of a comprehensive `build.cmd` for automated setup, configuration, and deployment.

## Consequences
- Every solution must include a `build.cmd` script for one-click deployment.
- Technical debt is minimized through early categorization and SOLID design enforcement.
- Prompt engineering is standardized for high-throughput model inference.
