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

export interface WaveformEvent {
  signal: string;
  timestamp: number;
  value: string;
}

export interface SimulationMetadata {
  timescale?: string;
  start_time?: number;
  end_time?: number;
  duration?: number;
  clock_signals?: string[];
  clock_periods?: Record<string, number>;
  clock_frequencies?: Record<string, string>;
}

export interface SignalActivity {
  transitions: number;
}

export interface WaveformResult {
  status: "success" | "error" | "empty" | "unavailable" | "PASSED";
  source?: "generated" | "uploaded" | "none" | string;
  events_count: number;
  signals_analyzed: string[];
  events?: WaveformEvent[];
  observations?: WaveformObservation[];
  message?: string;
  simulation?: SimulationMetadata;
  signal_activity?: Record<string, SignalActivity>;
}

export interface SignalMetadata {
  name: string;
  direction: "input" | "output" | "internal" | string;
  data_type: string;
  width: number;
  signed: boolean;
}

export interface DesignMetadata {
  top_module: string;
  module_count: number;
  instance_count: number;
  port_count: number;
  signal_count: number;
  input_count: number;
  output_count: number;
  parameter_count: number;
  assignment_count: number;
  always_block_count: number;
  operation_counts: Record<string, number>;
  signals: SignalMetadata[];
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
  design_metadata?: DesignMetadata;
  diagnostics: Diagnostic[];
  hierarchy: HierarchyNode[];
  traceability: TraceabilityLink[];
  waveform: WaveformResult;
  explanation: AIExplanation;
  reports: Reports;
}
