# 07 - Coding Standards

## Engineering Guidelines

### 1. Backend (Python 3.10+)
- **Strict Typing**: All functions, methods, and dataclasses must use complete `typing` annotations (`Optional`, `Union`, `List`, `Dict`, `Tuple`).
- **Immutability Where Possible**: Diagnostic records and AST tokens are immutable value objects to prevent state corruption during analysis passes.
- **Error Handling**: Never raise unhandled exceptions during parsing. Syntax anomalies must be recorded into the diagnostic sink and compilation must proceed to downstream stages when possible.
- **Testing**:
  - Unit tests placed under `backend/tests/`.
  - Smoke tests and regression suites runnable via `pytest backend/tests`.

### 2. Frontend (React 19 / TypeScript)
- **Component Architecture**: Modular component breakdown with clear separation of UI presentation, state hooks, and API services.
- **Styling**: Modern dark workstation aesthetic using Tailwind CSS utility classes and centralized theme tokens.
- **Safety**: Strict TypeScript type checking (`strict: true` in `tsconfig.json`), no untyped `any` in core state management.
