import { Info } from 'lucide-react';
import { KiwiAssistantWidget } from '../common/KiwiAssistantWidget';
import { RivaIntelligencePanel } from '../ai/RivaIntelligencePanel';
import type { InputStatus, AnalysisState } from '../../types/state';

interface ContextPanelProps {
  activeSection: string;
  inputStatus: InputStatus;
  analysisState: AnalysisState;
}

const SECTION_CONTEXT: Record<string, { label: string; description: string }> = {
  overview:      { label: 'Overview',       description: 'Check input readiness and start verification.' },
  specification: { label: 'Specification',  description: 'Paste or load your requirement file. Use [REQ-NNN] format for traceability.' },
  rtl:           { label: 'RTL',            description: 'SystemVerilog RTL is parsed and semantically analyzed by the backend engine.' },
  testbench:     { label: 'Testbench',      description: 'Optional: Simulation stimulus for waveform-linked verification.' },
  waveform:      { label: 'Waveform (VCD)', description: 'Optional: VCD trace analyzed by the backend waveform engine.' },
  analysis:      { label: 'Analysis',       description: 'Verification pipeline status.' },
  results:       { label: 'Results',        description: 'Grounded backend verification results, hierarchy, traceability, and AI explanation.' },
  reports:       { label: 'Reports',        description: 'Backend-generated consolidated Markdown and JSON verification reports.' },
};

export function ContextPanel({ activeSection, inputStatus, analysisState }: ContextPanelProps) {
  const ctx = SECTION_CONTEXT[activeSection] ?? SECTION_CONTEXT['overview'];

  return (
    <aside className="w-72 bg-[#0A0D0E] border-l border-slate-800/70 flex flex-col flex-shrink-0 h-full overflow-hidden">
      {/* 1. Context Information Header */}
      <div className="p-4 border-b border-slate-800 space-y-2 flex-shrink-0">
        <div className="flex items-start gap-2">
          <Info className="w-3.5 h-3.5 text-slate-500 mt-0.5 flex-shrink-0" />
          <div>
            <p className="text-xs font-semibold text-slate-300">{ctx.label}</p>
            <p className="text-[11px] text-slate-500 leading-relaxed mt-0.5">{ctx.description}</p>
          </div>
        </div>
      </div>

      {/* 2. Input Status Summary */}
      <div className="p-4 border-b border-slate-800/60 flex-shrink-0">
        <p className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-2.5">Input Status</p>
        <div className="space-y-1.5 font-mono text-[11px]">
          {[
            { label: 'Specification', has: inputStatus.hasSpecification, req: true },
            { label: 'RTL',           has: inputStatus.hasRTL,           req: true },
            { label: 'Testbench',     has: inputStatus.hasTestbench,     req: false },
            { label: 'Waveform',      has: inputStatus.hasWaveform,      req: false },
          ].map(({ label, has, req }) => (
            <div key={label} className="flex justify-between">
              <span className="text-slate-600">{label}</span>
              <span className={has ? 'text-emerald-400' : req ? 'text-amber-600/70' : 'text-slate-700'}>
                {has ? '● Ready' : req ? '○ Empty' : '○ Optional'}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* 3. Main RIVA Intelligence Panel (Scrollable Body) */}
      <div className="flex-1 overflow-y-auto">
        <RivaIntelligencePanel analysisState={analysisState} />
      </div>
      {/* 4. Kiwi Assistant Footer Widget */}
      <div className="p-3 border-t border-slate-800 flex-shrink-0">
        <KiwiAssistantWidget />
      </div>
    </aside>
  );
}
