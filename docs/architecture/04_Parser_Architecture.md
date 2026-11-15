# 04 - Parser Architecture

## SystemVerilog Parser Subsystem

The RIVA parser processes a synthesizable IEEE 1800 SystemVerilog subset into a strongly typed AST.

### Pipeline Stages

```
Raw HDL Text ──► Lexer (Tokenization) ──► Macro Preprocessor ──► Concrete Parser ──► AST Lowering
```

1. **Lexical Analysis (`app/parsers/rtl/`)**:
   - Tokenizes SystemVerilog keywords, operators, identifiers, integer literals (`32'hDEAD_BEEF`), and strings.
   - Preserves 1-based source coordinate spans (`line`, `column`, `end_line`, `end_column`) on every emitted token.

2. **Macro & Include Preprocessor (`app/preprocessors/rtl/`)**:
   - Resolves `` `define `` macros, conditional compilation (`` `ifdef ``, `` `ifndef ``, `` `elsif ``, `` `endif ``), and file inclusions (`` `include ``).

3. **AST Construction (`app/ast/`)**:
   - Synthesizes recursive AST hierarchy:
     - `CompilationUnit`: Root containing one or more modules.
     - `ModuleDeclaration`: Encapsulates ports, parameters, signals, and internal blocks.
     - `AlwaysBlock`: Supports `always @(*)`, `always_comb`, `always_ff @(posedge clk or negedge rst_n)`, and `always_latch`.
     - `ProceduralAssignment`: Models blocking (`=`) and non-blocking (`<=`) assignments.
     - `IfStatement` & `CaseStatement`: Captures multi-branch conditional logic and default branches.
     - `GenerateBlock`: Supports `generate for` loops and `generate if` branches.

4. **Error Recovery**:
   - Employs synchronizing token recovery on syntax anomalies, preventing parser crashes and collecting multiple errors in a single compilation pass.
