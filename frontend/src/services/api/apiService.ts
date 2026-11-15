import type { AnalyzeRequest, AnalyzeResponse } from "../../types/api";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export class ApiService {
  static async analyze(request: AnalyzeRequest): Promise<AnalyzeResponse> {
    let response: Response;
    try {
      response = await fetch(`${API_BASE_URL}/api/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          rtl_code: request.rtl_code,
          spec_code: request.spec_code,
          testbench_code: request.testbench_code,
          vcd_content: request.vcd_content ?? "",
        }),
      });
    } catch (networkErr) {
      throw new Error("RIVA backend is unavailable. Ensure the backend is running on " + API_BASE_URL, { cause: networkErr });
    }

    if (response.status === 422) {
      throw new Error("Verification request was rejected by the backend (validation error).");
    }
    if (response.status === 400) {
      throw new Error("Verification request was rejected. Check your input for obvious errors.");
    }
    if (!response.ok) {
      throw new Error(`RIVA returned an unexpected response (HTTP ${response.status}).`);
    }

    let data: unknown;
    try {
      data = await response.json();
    } catch {
      throw new Error("RIVA returned a malformed response. Please retry.");
    }

    return data as AnalyzeResponse;
  }

  static async kiwiChat(payload: { messages: Array<{ role: string; content: string }>; project_context: Record<string, unknown> }): Promise<{ text: string; provider: string; live_ai: boolean }> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/kiwi/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (response.ok) {
        return await response.json();
      }
    } catch {
      // Fallback response if network error
    }
    return {
      text: "Unable to connect to Kiwi assistant backend service. Please check network connection.",
      provider: "offline",
      live_ai: false,
    };
  }

  static async checkHealth(): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/`, { method: "GET" });
      return response.ok;
    } catch {
      return false;
    }
  }
}
