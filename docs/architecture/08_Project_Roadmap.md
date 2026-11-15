# 08 - Project Roadmap & Milestones

## Project Status & Development Phases

Developed as an advanced Project Based Learning (PBL) initiative at **Chennai Institute of Technology (CIT)** under the Department of Electronics and Communication Engineering.

| Phase | Milestone | Scope & Deliverables | Status |
|---|---|---|---|
| **Phase 1** | **Review 1** | Problem definition, literature survey, baseline AST parser & initial rule catalog | **Completed** |
| **Phase 2** | **Review 2** | Semantic width inference, latch & FSM rules, grounded AI repair, Kiwi assistant | **Completed** |
| **Phase 3** | **Review 3 (Final)** | QuestaSim/Vivado closed-loop regression, full workstation UI, hardware benchmarks | **Under Active Development** |

### Milestone Breakdown

- [x] Synthesizable SystemVerilog Lexer and AST Generator
- [x] Bit-width & Signedness Inference Engine
- [x] AST Lint Rules (Latches, Truncation, Dead Code, Multiple Drivers)
- [x] Grounded Evidence Store (Anti-Hallucination Sandbox)
- [x] Multi-Provider AI Repair Engine (Gemini / OpenAI / Anthropic / Offline Fallback)
- [x] Kiwi Conversational RTL Assistant
- [x] Interactive Verification Workstation (React + Vite + Monaco + VCD Waveform)
- [ ] Direct Vivado & QuestaSim TCP Automation Bridge
- [ ] Formal Property Checking (SVA) Synthesis
