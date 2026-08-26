import type { AnalyzeResponse } from "./api";

export type AnalysisStatus = "idle" | "loading" | "success" | "error";

export interface ProjectState {
  projectName: string;
  rtlCode: string;
  specCode: string;
  testbenchCode: string;
  vcdContent: string;
  uploadedFileName: string;
  isDirtyRtl: boolean;
  isDirtySpec: boolean;
  isDirtyTb: boolean;
  isDirtyVcd: boolean;
}

export interface InputStatus {
  hasRTL: boolean;
  hasSpecification: boolean;
  hasTestbench: boolean;
  hasWaveform: boolean;
  isReadyForAnalysis: boolean;
}

export interface AnalysisState {
  status: AnalysisStatus;
  backendOnline: boolean;
  result: AnalyzeResponse | null;
  error: string | null;
}

export interface UIState {
  activeSection: string;
  consoleLogs: string[];
}
