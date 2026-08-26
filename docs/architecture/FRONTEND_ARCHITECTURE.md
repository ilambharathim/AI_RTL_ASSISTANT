# RIVA Frontend Architecture

## 1. Project Structure
The RIVA project enforces a strict separation between the backend verification engine and the frontend user interface.
- **Backend (`~/RIVA/backend`)**: Contains the verification engine, API, AI subsystems, and testing. Frozen and acts as a service.
- **Frontend (`~/RIVA/frontend`)**: Contains the React UI and communicates with the backend exclusively via REST API.
- **Docs (`~/RIVA/docs`)**: Contains all architecture and API documentation.

## 2. Responsibilities
- **Backend**: Responsible for parsing SystemVerilog, analyzing semantics, resolving types, inferring width/signedness, tracking diagnostics, integrating with VCD waveforms, parsing specifications for traceability, and querying the AI reasoning engine.
- **Frontend**: Responsible for presenting analysis results, maintaining editors for code/specs/testbenches, and providing a cohesive, responsive UX. The frontend holds zero simulation or verification logic.

## 3. Component Organization
The frontend `src` folder is organized modularly:
- `assets/`: Static media.
- `components/`: UI components organized by domain:
  - `layout/`: Shell frame, header, sidebar, context panel, status bar.
  - `editor/`: Verification workspace, editor toolbar, input tabs, overview tab.
  - `analysis/`: Progress spinner, error display, consolidated results view.
  - `results/`: Verification summary, diagnostic overview, diagnostic list, diagnostic cards.
  - `hierarchy/`: Hierarchy explorer, hierarchy tree nodes.
  - `traceability/`: Requirement traceability explorer, requirement trace cards.
  - `waveform/`: Waveform panel, activity metrics, signal list, observation cards.
  - `ai/`: RIVA Intelligence panel, grounded AI findings cards, confidence badges.
  - `repair/`: Guided repair panel, repair suggestion cards.
  - `reports/`: Report center — backend Markdown/JSON preview, copy, download, print.
  - `common/`: Status indicators, empty states, Kiwi assistant widget.
- `hooks/`: Custom React hooks for state and lifecycle (`useRivaState`).
- `services/`: API clients and external communications (`apiService.ts`).
- `styles/`: Core application styles (`index.css`).
- `types/`: Shared TypeScript models corresponding to backend payloads (`api.ts`, `state.ts`).

## 4. API Communication & Data Flow
The UI strictly delegates processing to the `ApiService` which posts to the `POST /api/analyze` endpoint.
The state flows as:
1. User interacts with editors -> Local state updates (`ProjectState`).
2. User submits -> `ApiService.analyze()` is called with `AnalyzeRequest`.
3. Backend processes and returns `AnalyzeResponse`.
4. The response updates `AnalysisState`.
5. UI components react to `AnalysisState`, rendering results in order: Verification Summary → Diagnostics → Guided Repair → Hierarchy Explorer → Traceability Explorer → Waveform Analysis → AI Reasoning Summary → Open Full Report.

## 5. Phase 5 — Hierarchy & Traceability Visualizations
- **Hierarchy Explorer (`src/components/hierarchy/`)**: Renders elaborated SystemVerilog design hierarchy recursively using backend `result.hierarchy` tree nodes (`module_name`, `instance_name`, `parameters`, `children`). Features expand/collapse toggles and single-module fallback rendering.
- **Traceability Explorer (`src/components/traceability/`)**: Renders specification traceability links from backend `result.traceability` (`requirement_id`, `signal_name`, `expected`, `actual`, `status`). Features requirement status badges (`PASSED`/`FAILED`), filtering tabs (`All`, `Passed`, `Failed`), card selection states, and safe linkage to failed diagnostics (`RIVA6002`).

## 6. Phase 6 — Waveform / VCD Visualization
- **Waveform Pipeline**:
  ```text
  VCD Input → POST /api/analyze → backend WaveformAnalyzer → AnalysisState.result.waveform → WaveformPanel
  ```
- **Waveform Panel (`src/components/waveform/`)**: Visualizes backend waveform payload (`status`, `events_count`, `signals_analyzed`, `observations`, `observations_raw`).
- **No VCD Parsing in Frontend**: The frontend does not parse VCD files or fabricate signal transitions. If no VCD is provided, a clear *"No waveform provided"* empty state is shown. If VCD parsing fails on the backend, a *"Waveform Analysis Error"* card is rendered safely.

## 7. Phase 7 — Grounded AI Assistant / Intelligence Experience
- **Grounded AI Pipeline**:
  ```text
  Backend Evidence Store → Grounding Validator → AnalyzeResponse.explanation → AnalysisState → RivaIntelligencePanel
  ```
- **RivaIntelligencePanel (`src/components/ai/`)**: Displays the backend's verified AI explanation summary, confidence score, and findings cards.
- **No Frontend AI Generation**: The frontend does not generate AI explanations, make LLM calls, or invent finding details. React only renders `result.explanation` and links finding items to matching diagnostics (`finding.code === diagnostic.code`).

## 8. Phase 8 — Guided Repair Experience
- **Guided Repair Pipeline**:
  ```text
  Diagnostic → Evidence Location → Grounded AI Explanation → Suggested Fix → Guided Repair Panel → Engineer Approval / Copy / Return to Editor
  ```
- **Repair Center (`src/components/repair/`)**: Displays actionable guided repair recommendation cards for each diagnostic violation. Provides a *"Copy Suggested Fix"* button and a *"Return to RTL Editor"* navigation action.
- **No Automatic RTL Mutation**: The frontend does not generate code patches, apply automatic regex replacements, or modify user RTL files. If no backend patch replacement payload exists, the UI explicitly displays *"Automated code patch preview is not available for this diagnostic."* while maintaining engineer control.

## 9. Phase 9 — Reports / Export / Verification Evidence
- **Report Generation Pipeline**:
  ```text
  ConsolidatedReportGenerator (backend)
      ↓  generates
  AnalyzeResponse.reports.markdown  (str — backend-authored Markdown)
  AnalyzeResponse.reports.json      (str — JSON.dumps of evidence + AI reasoning)
      ↓  stored in
  AnalysisState.result.reports
      ↓  rendered in
  ReportCenter (src/components/reports/)
  ```
- **ReportCenter (`src/components/reports/ReportCenter.tsx`)**: Displays the backend-generated report in two tabs — Markdown Report and JSON Report. Provides Copy, Download (Blob), and Print (native browser) actions for both formats.
- **Report Header**: Displays project name, top module, verification status, diagnostic counts, requirements passed/total, waveform availability, and AI confidence score — all sourced from `AnalysisState.result` without recalculation.
- **No Frontend Report Generation**: The frontend does NOT generate, reconstruct, or alter the Markdown or JSON report. `result.reports.markdown` and `result.reports.json` are rendered verbatim from the backend. The Report Center is a read-only presentation layer.
- **Security**: Report content is rendered using safe React text (`<pre>` elements). `dangerouslySetInnerHTML` is never used for report content.
- **Navigation**: A `Reports` sidebar item (disabled until analysis succeeds) provides direct access. An `[Open Full Report]` button at the bottom of the Results view links to the Report Center. Reports section also correctly handles idle (NO REPORT AVAILABLE), error (REPORT UNAVAILABLE), and loading states.
- **Stale Report Prevention**: Report content derives entirely from `AnalysisState.result.reports`. Because `AnalysisState` is overwritten on each verification run, no stale report data is ever shown from a previous run.
- **Download Filenames**: `{projectName}-report.md` and `{projectName}-report.json` using browser Blob API. No server-side file generation.

## 10. Phase 10 — Final UX Polish
Phase 10 changes are **presentation-only** and do not alter backend contracts, verification semantics, API payloads, diagnostic logic, AI reasoning, repair behavior, or report generation.

### Global Polish
- **CSS**: Expanded `index.css` with Inter 300-700 + JetBrains Mono 400-600 font weights, `:focus-visible` ring for keyboard accessibility, `@media (prefers-reduced-motion: reduce)` support, `@media print` styles, CSS animation keyframes for atmospheric glow, and improved scrollbar styling.
- **Typography hierarchy**: Application title → Section title → Card title → Technical metadata → Supporting text. Consistent use of `tabular-nums` for numeric values.
- **Spacing rhythm**: Consistent `rounded-xl`/`rounded-lg` borders, `p-4`/`p-5` card padding, `gap-2`/`gap-3` button spacing, and `text-[10px]`/`text-[11px]` label sizing throughout all components.

### Component Improvements
- **RivaHeader**: Gradient logo mark, improved backend status colors with contextual background, cleaner typography stack.
- **Sidebar**: Grouped navigation (Inputs / Analysis) with section labels, improved active state styling, dot badge for passing results, `focus-visible` rings, disabled tooltips.
- **OverviewTab**: Table-style input readiness with `AlertCircle` for missing required inputs, integrated status badge, clearer CTA.
- **EditorToolbar**: Consistent button sizing with focus rings, `Dot` icon for unsaved state, responsive line/char counts, truncated subtitles.
- **StatusBar**: Compacted to 28px height, icon+number pairs instead of label+value, `no-print` class.
- **VerificationSummary**: `ShieldCheck` icon, tabular-nums metrics, refined severity color mapping.
- **DiagnosticOverview**: Icons for error/warning counts, improved filter tab focus states.
- **AnalysisProgress**: Layered spinner ring with pulse inner circle, better text hierarchy.
- **AnalysisError**: Improved focus ring, consistent button styling.
- **ContextPanel**: Narrowed to 288px, added Reports section context, consistent `#0A0D0E` background.
- **RivaShell**: Subtler atmospheric glow with `riva-bg-glow` animation, dimmer placeholder text colors, top-left gradient origin.
- **VerificationWorkspace**: Removed stale Phase 3 placeholder text.
