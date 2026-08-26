import { CheckCircle2, Circle, Play, AlertCircle } from 'lucide-react';
import type { ProjectState, InputStatus } from '../../types/state';

interface OverviewTabProps {
  projectState: ProjectState;
  inputStatus: InputStatus;
  onStartVerification: () => void;
}

const inputRows = [
  { key: 'hasSpecification' as const, label: 'Specification',       sub: 'Natural language requirements', required: true  },
  { key: 'hasRTL'           as const, label: 'SystemVerilog RTL',   sub: 'Hardware implementation',      required: true  },
  { key: 'hasTestbench'     as const, label: 'Testbench',           sub: 'Simulation stimulus module',   required: false },
  { key: 'hasWaveform'      as const, label: 'Waveform (VCD)',      sub: 'Value change dump trace',      required: false },
];

export function OverviewTab({ projectState, inputStatus, onStartVerification }: OverviewTabProps) {
  const requiredMissing = !inputStatus.hasRTL || !inputStatus.hasSpecification;

  return (
    <div className="max-w-2xl mx-auto w-full mt-8 flex flex-col gap-6">
      {/* Project identity */}
      <div className="flex items-center gap-4 border-b border-slate-800/60 pb-6">
        <div className="w-14 h-14 bg-[#0F1516] border border-cyan-900/40 rounded-xl flex items-center justify-center shadow-[0_0_18px_rgba(34,211,238,0.08)] flex-shrink-0">
          <span className="text-2xl font-black text-cyan-400">R</span>
        </div>
        <div>
          <h1 className="text-xl font-bold text-slate-100 tracking-tight leading-tight">{projectState.projectName}</h1>
          <p className="text-sm text-slate-500 mt-0.5">Verification Input Workspace</p>
        </div>
      </div>

      {/* Input readiness */}
      <div className="bg-slate-900/30 border border-slate-800/80 rounded-xl overflow-hidden">
        <div className="px-5 py-3.5 border-b border-slate-800/60 flex items-center justify-between">
          <h2 className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">Input Readiness</h2>
          <span className={`text-[10px] font-mono px-2 py-0.5 rounded border font-semibold ${
            inputStatus.isReadyForAnalysis
              ? 'bg-emerald-950/30 text-emerald-400 border-emerald-900/40'
              : 'bg-amber-950/20 text-amber-500 border-amber-900/30'
          }`}>
            {inputStatus.isReadyForAnalysis ? 'Ready to verify' : 'Required inputs missing'}
          </span>
        </div>

        <div className="divide-y divide-slate-800/50">
          {inputRows.map(({ key, label, sub, required }) => {
            const isReady = inputStatus[key];
            return (
              <div key={key} className="flex items-center justify-between px-5 py-3.5 hover:bg-slate-800/20 transition-colors">
                <div className="flex flex-col gap-0.5">
                  <span className="text-sm font-medium text-slate-200">{label}</span>
                  <span className="text-[11px] text-slate-600">
                    {sub} {required ? '— Required' : '— Optional'}
                  </span>
                </div>
                <div className="flex items-center gap-2.5 flex-shrink-0 ml-4">
                  <span className={`text-[11px] font-mono font-medium ${isReady ? 'text-emerald-400' : required ? 'text-amber-500' : 'text-slate-600'}`}>
                    {isReady ? 'Ready' : required ? 'Empty' : 'Optional'}
                  </span>
                  {isReady
                    ? <CheckCircle2 className="w-4.5 h-4.5 text-emerald-500" />
                    : required
                    ? <AlertCircle className="w-4.5 h-4.5 text-amber-500/60" />
                    : <Circle className="w-4.5 h-4.5 text-slate-700" />
                  }
                </div>
              </div>
            );
          })}
        </div>

        {/* Start Verification CTA */}
        <div className="px-5 py-4 border-t border-slate-800/60 bg-slate-900/20 flex items-center justify-between gap-4">
          {requiredMissing && (
            <p className="text-[11px] text-amber-500/80 font-mono">
              Add Specification and RTL to proceed.
            </p>
          )}
          <div className="ml-auto">
            <button
              type="button"
              id="btn-start-verification"
              disabled={!inputStatus.isReadyForAnalysis}
              onClick={onStartVerification}
              className={`flex items-center gap-2 px-5 py-2.5 rounded-lg font-semibold text-sm transition-all duration-150 focus-visible:ring-2 focus-visible:ring-emerald-500/60 ${
                inputStatus.isReadyForAnalysis
                  ? 'bg-emerald-700/25 text-emerald-400 border border-emerald-600/40 hover:bg-emerald-700/35 hover:border-emerald-500/60 shadow-[0_0_16px_rgba(52,211,153,0.08)]'
                  : 'bg-slate-800/40 text-slate-600 border border-slate-700/60 cursor-not-allowed opacity-60'
              }`}
            >
              <Play className="w-4 h-4" />
              Start Verification
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
