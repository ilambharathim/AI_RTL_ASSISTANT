# RIVA Development Rules

## Mission
Build an industry-grade SystemVerilog RTL analysis, diagnostics, elaboration, optimization, simulation, and AI-assisted debugging platform.

## Core Rules
1. Never assume. Inspect the code first.
2. Compile after every meaningful change.
3. Run targeted tests before running the full suite.
4. Fix root causes, never patch symptoms.
5. Do not remove existing functionality unless verified.
6. Always inspect architecture before modifying it.
7. Keep the implementation aligned with IEEE SystemVerilog specifications.
8. Always check for duplicate implementations and obsolete code.
9. Keep Git commits small and meaningful.
10. Every change must be verified before moving to the next step.

## Standard Workflow
1. Inspect architecture.
2. Inspect affected files.
3. Make one change.
4. Compile.
5. Run related tests.
6. Fix failures.
7. Run full validation.
8. Commit.
9. Push.

## Bash First
Always provide terminal commands in Bash whenever possible.

## Verification Policy
- python -m py_compile
- python -m compileall
- pytest (targeted)
- pytest (full)
- Manual verification if required

## Reminder
We are building a professional engineering tool, not a college project.
