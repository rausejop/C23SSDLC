# ADR-002: Stack and Operational Directives

## Date
2026-01-25

## Status
Accepted

## Context
To ensure consistency, maintainability, and high-performance in the C23 Software Factory, a unified technology stack and operational guidelines are required.

## Decision
We will adhere to the following strict stack and directives:
- **Language**: Python 3.14.2. Although it is not the current stable version (unlike 3.13), we choose it as the latest available version to leverage cutting-edge features.
- **Dependency Management**: Due to the choice of Python 3.14.2, modern tools like `uv` are not yet compatible. Therefore, we will continue to use `pip` and `requirements.txt` for dependency management.
- **Asynchronicity**: Native `asyncio` mandatory for all I/O and Model Inference calls.
- **Logging**: Structured JSON logging via `loguru` with mandatory console debug output.
- **Documentation**: Google-style Docstrings and PEP 484/526 Type Hints required for all code.

## Consequences
- Developers must use Python 3.14.2, assuming potential stability risks associated with a non-LTS/stable release.
- **Incompatibility**: High-performance dependency managers like `uv` cannot be used; `pip` remains the standard.
- Legacy synchronous code must be refactored or wrapped to comply with `asyncio` standards.
- Documentation and type hints are strictly enforced through CI/CD linting.
- Standardized logging facilitates observability across all services.
