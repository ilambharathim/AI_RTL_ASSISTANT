# RIVA Supported SystemVerilog RTL Subset Specification

RIVA (RTL Intelligent Verification Assistant) operates deterministically over a formal, production-grade subset of the IEEE 1800-2023 SystemVerilog language standard.

---

## 1. Supported Language Constructs

### Module Declarations & Headers
- ANSI and non-ANSI port declarations (`input`, `output`, `inout`).
- Data types: `logic`, `bit`, `reg`, `wire`, `int`, `integer`.
- Vector bus ranges: packed dimensions `[MSB:LSB]`, unsized scalars.
- Parameter declarations: `parameter`, `localparam` with expressions.

### Procedural & Continuous Assignments
- Continuous assignments: `assign dst = expression;`
- Combinational procedural blocks: `always_comb`, `always @(*)` with blocking assignments (`=`).
- Sequential procedural blocks: `always_ff @(posedge clk or posedge reset)`, `always @(posedge clk)` with non-blocking assignments (`<=`).

### Control Flow Constructs
- Conditional statements: `if`, `else if`, `else` (nested and chained).
- Multi-way branching: `case`, `casez`, `casex` with `default` branches.
- Procedural `begin ... end` blocks with statement scoping.

### Generate & Hierarchy Constructs
- Conditional generate: `generate if (condition) ... else ... endgenerate`
- Iterative generate: `generate for (genvar i = 0; i < N; i++) ... endgenerate`
- Module instantiations: named port connections `.port_name(signal_name)`, positional connections, parameter overrides `#(.PARAM(val))`.

### Expressions & Operators
- Arithmetic: `+`, `-`, `*`, `/`, `%`
- Bitwise & Logical: `&`, `|`, `^`, `~^`, `~`, `&&`, `||`, `!`
- Relational & Equality: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Shift: `<<`, `>>`, `<<<`, `>>>`
- Concatenation & Bit Selection: `{a, b}`, `bus[7:0]`, `bus[idx]`
- Sized & Unsized Literals: `16'h1234`, `8'd255`, `4'b1010`, `1'b1`, `'0`, `'1`
- Signedness: `signed`, `unsigned` keywords and signed literal interactions.

---

## 2. Deterministic Verification Rules Enforced

1. **RIVA1001**: Undefined identifier / signal reference.
2. **RIVA2003**: Bit-width mismatch (procedural assignment truncation, port connection width mismatch).
3. **RIVA2004**: Signedness mismatch (signed vs unsigned destination assignment).
4. **RIVA6001**: Specification requirement violation (`[REQ-xxx]` expected vs actual bit-width or signal type mismatch).

---

## 3. Grounded AI Evidence Engine Architecture

RIVA enforces a strict downstream AI architecture:
- **Phase 1**: Deterministic compiler analysis (Lexer -> AST Parser -> Semantics -> CFG -> Traceability).
- **Phase 2**: Structuring facts into an immutable `EvidencePayload`.
- **Phase 3**: LLM Grounded Explanation Generation. The AI engine is strictly constrained to reason over facts produced in Phase 2 and cannot invent unemitted diagnostics.
