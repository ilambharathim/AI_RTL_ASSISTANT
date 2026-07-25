# RIVA Project Context

## 1. Project Identity

**RIVA** stands for **Requirement Intelligent Verification Assistant**.

RIVA is being developed as a serious hardware-design and verification
platform. It is not a demonstration-only application, a college prototype,
or a chatbot that generates unverifiable RTL.

The long-term goal is to transform engineering specifications and hardware
artifacts into structured intermediate representations that support:

- requirement extraction;
- RTL and interface understanding;
- verification planning;
- assertion generation;
- deterministic rule-based analysis;
- consistency checking;
- simulation and formal-verification integration;
- diagnostics and reporting;
- controlled AI-assisted engineering workflows.

Every extracted, inferred, or generated artifact should remain traceable to
its original source location.

## 2. Engineering Philosophy

RIVA follows a **deterministic-first** architecture.

Deterministic components are responsible for:

- reading and normalizing source files;
- lexical analysis and parsing;
- intermediate-representation construction;
- validation and rule execution;
- diagnostics;
- simulation and formal orchestration;
- reproducible reporting.

AI may augment these components, but it must not replace deterministic
parsing, validation, source tracking, or verification evidence.

AI should operate on structured representations rather than treating every
engineering input as unstructured text.

RIVA must distinguish between:

- directly extracted information;
- deterministic inference;
- heuristic inference;
- AI-generated suggestions;
- verified engineering results.

Generated content must never be silently presented as verified truth.

## 3. Planned Input Domains

RIVA will support engineering inputs through format-specific readers and
parser adapters.

Planned specification and documentation inputs include:

- plain text;
- Markdown;
- HTML;
- PDF;
- DOCX;
- Confluence content;
- IP-XACT.

Planned hardware and verification inputs include:

- SystemVerilog;
- Verilog;
- VHDL;
- SystemVerilog Assertions;
- UVM;
- UPF;
- SDC.

Accepting a filename extension does not mean semantic parsing for that
format is complete.

The generic specification lexer does not parse HDL or verification-language
syntax. Industrial RTL parsing will require dedicated parser integrations.

## 4. Current Repository Architecture

The active backend architecture is:

```text
backend/app/
  ai/
  api/
  config/
  domain/
    ast/
  engines/
    diagnostics/
    reporting/
    rule_engine/
    verification/
  infrastructure/
    uploads/
  knowledge/
  parsers/
    rtl/
    specification/
  schemas/
  shared/
  storage/
  tests/
  main.py
```

This architecture replaces the earlier V1 layout based on broad modules,
services, models, and orchestrator directories.

The current design separates domain models, parsers, infrastructure,
storage, APIs, verification engines, reporting, diagnostics, and AI.

Architecture changes require a compelling engineering reason, migration
tests, and a rollback checkpoint.

## 5. Current Specification Frontend

Implemented specification frontend components include:

- reader;
- normalizer;
- scanner;
- line reader;
- classifier;
- lexer rules;
- token builder;
- lexer;
- token model;
- token types;
- parser exceptions.

### Reader Status

The current reader supports UTF-8 plain-text input through a backend
registry.

Implemented reader behavior includes:

- UTF-8 reading;
- UTF-8 BOM removal;
- case-insensitive extension matching;
- missing-path rejection;
- directory-path rejection;
- unsupported-format errors;
- invalid UTF-8 error wrapping;
- custom reader-backend registration.

PDF and DOCX filenames may be accepted by upload validation, but production
PDF and DOCX reader backends have not yet been implemented.

### Lexer Status

The specification lexer performs deterministic generic document
tokenization.

Implemented lexer behavior includes:

- scanner and line-reader integration;
- generic structural token emission;
- key, colon, and value tokens;
- section-header tokens;
- list-item and text tokens;
- newline and EOF tokens;
- line and column tracking;
- source-file propagation;
- active-section propagation;
- LF and CRLF handling;
- final-line handling without a physical newline;
- repeatable tokenization;
- no debug-output side effects.

The lexer intentionally recognizes document structure only. Engineering
meaning belongs to later parser and semantic-builder stages.

## 6. Current Domain Models

Implemented domain components include:

- metadata;
- ports;
- requirements;
- specification IR;
- generic AST base node;
- document node;
- section node;
- key-value node;
- list-item node.

These models are an early foundation rather than a complete hardware
verification representation.

Future domain concepts are expected to include clocks, resets, parameters,
constraints, timing, assertions, protocols, interfaces, signals, finite-
state machines, RTL IR, and verification IR.

Empty implementation placeholders were intentionally removed. New files
should be added only when they contain real behavior or domain contracts.

## 7. Upload Infrastructure Status

Implemented upload behavior includes:

- category and filename validation;
- extension validation;
- unique stored filenames;
- temporary part files;
- flush and fsync before publication;
- atomic file replacement;
- rollback after partial upload failure;
- restricted deletion inside the upload root;
- API validation and storage-error handling.

Currently accepted extensions are:

- specification: PDF, DOCX, and TXT;
- RTL: SV and V;
- testbench: SV and V.

This is a baseline implementation, not a complete production upload
security boundary.

Future hardening should include configurable size limits, MIME and content
inspection, authentication, authorization, project ownership, audit logs,
configurable storage roots, retention policies, and object storage.

## 8. Testing Status

The backend currently uses standalone test scripts named test_*.py.

Current regression coverage includes:

- AST models;
- classifier;
- file storage and validation;
- specification reader;
- scanner and line reader;
- normalizer;
- deterministic specification lexer;
- domain models and specification IR;
- tokens and token builder;
- upload service and upload API.

The lexer has assertion-based tests for token order, values, source
locations, section context, indentation, blank lines, CRLF input, final
lines without physical newlines, repeated tokenization, invalid inputs,
and absence of debug output.

The complete backend regression passed at commit d487ff9.

Future testing improvements include migration to pytest, linting,
formatting, static type checking, coverage reporting, and CI execution.

## 9. Current Limitations

The following capabilities are not yet implemented:

- production generic parser;
- AST construction from lexer tokens;
- parser recovery and production diagnostics;
- semantic specification builder;
- complete Specification IR population from source documents;
- PDF and DOCX reader backends;
- Markdown, HTML, Confluence, and IP-XACT parsing;
- industrial RTL and HDL semantic parsing;
- SVA, UVM, UPF, and SDC analysis;
- requirement-to-RTL traceability;
- assertion and verification-plan generation;
- simulation and formal orchestration;
- production rule, diagnostics, and reporting engines;
- controlled AI workflow integration.

These limitations must not be hidden using placeholder implementations,
mocked success responses, or unsupported capability claims.

## 10. Near-Term Roadmap

The immediate specification-compiler roadmap is:

1. Generic parser.
2. Generic AST construction.
3. Parser diagnostics and recovery.
4. Semantic specification builder.
5. Specification IR population.
6. Traceability model.
7. Deterministic engineering validation rules.
8. Reporting and diagnostics integration.

After the specification pipeline is stable, RIVA should add format-specific
readers and industrial hardware-language parser adapters.

## 11. Development Protocol

When an issue is discovered, the expected workflow is:

```text
discover
  -> assess
  -> fix
  -> add focused regression
  -> run complete regression
  -> update documentation or dependencies
  -> create Git checkpoint
```

Implementation rules:

1. Do not add empty implementation placeholders.
2. Do not claim unsupported formats are semantically parsed.
3. Do not mix generic lexical structure with engineering semantics.
4. Do not let AI bypass deterministic validation.
5. Do not discard source-location information.
6. Do not commit debug output or failing regressions.
7. Do not make broad architecture changes without justification.
8. Keep changes focused, tested, documented, and checkpointed.
9. Record current limitations honestly.

## 12. Current Git Checkpoints

Active development branch:

```text
architecture-v2
```

Important implementation checkpoints:

```text
cefdf7b  refactor: establish RIVA architecture v2 foundation
d487ff9  feat: implement deterministic specification lexer
```

At the time this document was created, d487ff9 was the current code
checkpoint and the documentation file was the only uncommitted change.

## 13. Development Environment

Observed development environment:

```text
Operating system: Ubuntu 24.04
Python: 3.12.3
Repository: ~/RIVA
Backend: ~/RIVA/backend
Virtual environment: ~/RIVA/.venv
```

Typical activation sequence:

```bash
cd ~/RIVA
source .venv/bin/activate
cd backend
```

## 14. Source-of-Truth Rule

This document records the intended architecture and verified current state
of RIVA.

When implementation and documentation disagree:

1. Inspect the implementation and tests.
2. Determine whether the code or document is outdated.
3. Correct the inconsistency immediately.
4. Run the relevant regression.
5. Create a Git checkpoint.

Conversation memory must not be the only project record. Important
architecture decisions, limitations, and milestone status must be stored
in the repository.
