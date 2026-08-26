export interface AnalyzeRequest {
  rtl_code: string;
  spec_code: string;
  testbench_code: string;
  vcd_content?: string;
}

export interface Diagnostic {
  code: string;
  category: string;
  severity: "error" | "warning" | "info";
  message: string;
  suggestion: string;
  location: string;
}

export interface HierarchyNode {
  name?: string;
  type?: string;
  module_name?: string;
  instance_name?: string;
  parameters?: Record<string, string | number>;
  children?: HierarchyNode[];
}

export interface TraceabilityLink {
  requirement_id: string;
  signal_name: string;
  expected: string;
  actual: string;
  status: "PASSED" | "FAILED" | string;
}

export interface WaveformObservation {
  category: string;
  signal_name: string;
  message: string;
  timestamp: number;
}

export interface WaveformResult {
  status: "success" | "error" | "empty";
  events_count: number;
  signals_analyzed: string[];
  observations?: WaveformObservation[];
}

export interface AIFinding {
  code: string;
  location: string;
  explanation: string;
  suggested_fix: string;
}

export interface AIExplanation {
  summary: string;
  findings: AIFinding[];
  confidence_score: number;
}

export interface Reports {
  markdown: string;
  json: string;
}

export interface AnalyzeResponse {
  status: string;
  top_module: string;
  diagnostics: Diagnostic[];
  hierarchy: HierarchyNode[];
  traceability: TraceabilityLink[];
  waveform: WaveformResult;
  explanation: AIExplanation;
  reports: Reports;
}
