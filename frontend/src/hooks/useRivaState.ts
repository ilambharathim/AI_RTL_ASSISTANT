import { useState, useCallback, useMemo } from "react";
import type { ProjectState, AnalysisState, UIState, InputStatus } from "../types/state";
import type { AnalyzeResponse } from "../types/api";
import { ApiService } from "../services/api/apiService";

export function useRivaState() {
  const [projectState, setProjectState] = useState<ProjectState>({
    projectName: "RIVA Verification Project",
    rtlCode: "",
    specCode: "",
    testbenchCode: "",
    vcdContent: "",
    uploadedFileName: "design.sv",
    isDirtyRtl: false,
    isDirtySpec: false,
    isDirtyTb: false,
    isDirtyVcd: false,
  });

  const [analysisState, setAnalysisState] = useState<AnalysisState>({
    status: "idle",
    backendOnline: true,
    result: null,
    error: null,
  });

  const [uiState, setUiState] = useState<UIState>({
    activeSection: "overview",
    consoleLogs: [
      "[RIVA System] RIVA Enterprise Architecture initialized.",
      "[RIVA Engine] FastAPI backend endpoint configured.",
    ],
  });

  const addConsoleLog = useCallback((message: string) => {
    setUiState((prev) => ({
      ...prev,
      consoleLogs: [...prev.consoleLogs, message],
    }));
  }, []);

  const setActiveSection = useCallback((section: string) => {
    setUiState((prev) => ({ ...prev, activeSection: section }));
  }, []);

  const inputStatus = useMemo<InputStatus>(() => {
    const hasRTL = projectState.rtlCode.trim().length > 0;
    const hasSpecification = projectState.specCode.trim().length > 0;
    const hasTestbench = projectState.testbenchCode.trim().length > 0;
    const hasWaveform = projectState.vcdContent.trim().length > 0;
    const isReadyForAnalysis = hasRTL && hasSpecification;
    return { hasRTL, hasSpecification, hasTestbench, hasWaveform, isReadyForAnalysis };
  }, [projectState.rtlCode, projectState.specCode, projectState.testbenchCode, projectState.vcdContent]);

  const runAnalysis = useCallback(async () => {
    if (!inputStatus.isReadyForAnalysis) return;
    if (analysisState.status === "loading") return;

    setAnalysisState((prev) => ({ ...prev, status: "loading", result: null, error: null }));
    addConsoleLog("[RIVA] Starting verification pipeline...");

    try {
      const response: AnalyzeResponse = await ApiService.analyze({
        rtl_code: projectState.rtlCode,
        spec_code: projectState.specCode,
        testbench_code: projectState.testbenchCode,
        vcd_content: projectState.vcdContent,
      });

      setAnalysisState((prev) => ({
        ...prev,
        status: "success",
        result: response,
        error: null,
        backendOnline: true,
      }));
      addConsoleLog(`[RIVA] Verification complete. Top module: ${response.top_module}. Diagnostics: ${response.diagnostics.length}.`);
      setActiveSection("results");

    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "An unknown error occurred.";
      setAnalysisState((prev) => ({
        ...prev,
        status: "error",
        result: null,
        error: message,
        backendOnline: false,
      }));
      addConsoleLog(`[RIVA] Error: ${message}`);
    }
  }, [inputStatus.isReadyForAnalysis, analysisState.status, projectState, addConsoleLog, setActiveSection]);

  return {
    projectState,
    setProjectState,
    analysisState,
    setAnalysisState,
    uiState,
    setUiState,
    addConsoleLog,
    inputStatus,
    runAnalysis,
    setActiveSection,
  };
}
