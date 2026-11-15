# 05 - Verification Engine

## Static, Semantic, and Dynamic Verification

RIVA's verification engine is divided into three coordinated analysis subsystems:

### 1. Static Lint & AST Bug Detection
Identifies common synthesizability and behavioral pitfalls:
- **Unintended Latch Inference**: Flags combinational `always` blocks or `case` statements lacking exhaustive coverage or default branches where variables retain previous state.
- **Incomplete Finite-State Machines (FSM)**: Detects missing states, non-exhaustive state transitions, and undefined reset states.
- **Multiple Driver Conflicts**: Detects race conditions when signals are assigned across multiple concurrent processes or continuous assignments.
- **Dead Code / Unreachable Logic**: Locates constant condition branches that can never execute.

### 2. Semantic Width & Signedness Inference
- Evaluates expression operand bit-widths using IEEE 1800 sizing rules.
- Flags dangerous implicit bit truncations (e.g., assigning a 16-bit accumulator to an 8-bit bus without explicit slicing).
- Flags unexpected sign extension bugs occurring when mixing signed and unsigned operands in arithmetic operations.

### 3. Simulation-in-the-Loop Validation
- Integrates with simulation tools:
  - **Icarus Verilog (`iverilog` / `vvp`)**: Fast open-source regression.
  - **Siemens EDA QuestaSim / ModelSim**: Industry-standard golden simulation.
  - **AMD Xilinx Vivado Simulator (`xsim`)**: FPGA synthesis and simulation checks.
- Runs candidate patches automatically against golden testbenches.
- Verifies that zero assertions fail and functional coverage metrics are satisfied before certifying an auto-fix.
