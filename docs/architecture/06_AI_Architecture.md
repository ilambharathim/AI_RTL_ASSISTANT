# 06 - AI Architecture & Grounded Reasoning

## Eliminating AI Hallucination in RTL Verification

A fundamental design requirement of RIVA is **zero tolerance for synthetic hallucination**. Large Language Models operating on raw hardware code frequently invent invalid signal names, generate non-synthesizable syntax, or misinterpret clock domains.

### Grounded Context Isolation

To ensure complete reliability, RIVA isolates AI reasoning inside a strict sandbox:

```
[ AST + Scope Table ] ──► [ Evidence Slicer ] ──► [ Grounded Prompt ] ──► [ LLM Fix Engine ]
                                                          │                        │
                                                          │ Verified Facts Only    │ Candidate Patch
                                                          ▼                        ▼
                                                  [ AST Substitution ] ──► [ Simulation Loop ]
```

1. **Deterministic Pre-Filtering**:
   - The AI engine never parses raw RTL from scratch. The deterministic parser first establishes symbol definitions, bit-widths, and exact error locations.
2. **Context Grounding (`EvidenceStore`)**:
   - The prompt contains only:
     - Exact AST slice of the buggy code region.
     - Deterministic diagnostic rule ID (e.g. `LATCH-001`).
     - Declared port & signal bit-widths in the current scope.
     - Extracted specification contract requirements.
3. **Multi-Model Provider Support (`KiwiAIProviderManager`)**:
   - **Google Gemini API** (`gemini-1.5-pro` / `gemini-2.0-flash`): High-throughput code reasoning.
   - **OpenAI API** (`gpt-4o`): Precise structural patch generation.
   - **Anthropic API** (`claude-3-5-sonnet`): Advanced hardware architecture analysis.
   - **Grounded Fallback Engine**: If no external API keys are configured, RIVA automatically activates its deterministic template-based patch generator, providing reliable bug repairs completely offline.
