import { useState } from 'react';
import { FileCheck2, ArrowRight } from 'lucide-react';
import { VerificationSummary } from '../results/VerificationSummary';
import { DesignOverviewPanel } from '../results/DesignOverviewPanel';
import { DiagnosticOverview } from '../results/DiagnosticOverview';
import type { DiagnosticFilter } from '../results/DiagnosticOverview';
import { DiagnosticList } from '../results/DiagnosticList';
import { RepairPanel } from '../repair/RepairPanel';
import { HierarchyExplorer } from '../hierarchy/HierarchyExplorer';
import { TraceabilityExplorer } from '../traceability/TraceabilityExplorer';
import { WaveformPanel } from '../waveform/WaveformPanel';
import { AIInsightSummary } from '../results/AIInsightSummary';
import type { AnalyzeResponse } from '../../types/api';

interface AnalysisResultSummaryProps {
  result: AnalyzeResponse;
  onNavigateToEditor?: () => void;
  onNavigateToReports?: () => void;
}

export function AnalysisResultSummary({ result, onNavigateToEditor, onNavigateToReports }: AnalysisResultSummaryProps) {
  const [filter, setFilter] = useState<DiagnosticFilter>('all');
  const [selectedRepairCode, setSelectedRepairCode] = useState<string | null>(null);

  if (!result) {
    return (
      <div className="flex h-full items-center justify-center p-8 text-center text-slate-500 font-mono text-sm">
        No verification results yet. Run verification to analyze your design.
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto w-full py-4 space-y-6">
      {/* 1. Verification Summary */}
      <VerificationSummary result={result} />

      {/* 1.5. Design Overview (Metadata & Signal Intelligence) */}
      <DesignOverviewPanel metadata={result.design_metadata} />

      {/* 2. Diagnostics */}
      {result.diagnostics && result.diagnostics.length > 0 && (
        <div className="space-y-3">
          <DiagnosticOverview
            diagnostics={result.diagnostics}
            activeFilter={filter}
            onFilterChange={setFilter}
          />
          <DiagnosticList
            diagnostics={result.diagnostics}
            explanation={result.explanation}
            activeFilter={filter}
            onViewRepair={(code) => setSelectedRepairCode(code)}
          />
        </div>
      )}

      {/* 3. Guided Repair Panel */}
      <RepairPanel
        diagnostics={result.diagnostics}
        explanation={result.explanation}
        selectedCode={selectedRepairCode}
        onNavigateToEditor={onNavigateToEditor}
      />

      {/* 4. Design Hierarchy */}
      <HierarchyExplorer
        hierarchy={result.hierarchy}
        topModule={result.top_module}
      />

      {/* 5. Requirement Traceability */}
      <TraceabilityExplorer
        traceability={result.traceability}
        diagnostics={result.diagnostics}
      />

      {/* 6. Waveform Analysis */}
      <WaveformPanel waveform={result.waveform} />

      {/* 7. AI Explanation */}
      {result.explanation?.summary && (
        <AIInsightSummary explanation={result.explanation} />
      )}

      {/* 8. Open Full Report Action Bar */}
      {onNavigateToReports && (
        <div className="p-4 rounded-xl border border-slate-800 bg-[#0B0F10] flex items-center justify-between font-mono text-xs">
          <div className="flex items-center gap-2">
            <FileCheck2 className="w-4 h-4 text-cyan-400" />
            <span className="text-slate-300 font-semibold">Consolidated Verification Report Ready</span>
          </div>
          <button
            type="button"
            onClick={onNavigateToReports}
            className="px-4 py-2 rounded bg-cyan-900/40 hover:bg-cyan-900/60 border border-cyan-800/60 text-cyan-400 font-bold transition flex items-center gap-2"
          >
            <span>Open Full Report</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      )}
    </div>
  );
}
