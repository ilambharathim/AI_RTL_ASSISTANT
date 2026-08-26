import { AlertCircle, AlertTriangle, CheckCircle, Server, Activity } from 'lucide-react';
import type { AnalysisState, InputStatus } from '../../types/state';

interface StatusBarProps {
  analysisState: AnalysisState;
  inputStatus: InputStatus;
}

export function StatusBar({ analysisState, inputStatus }: StatusBarProps) {
  const { status, result, backendOnline } = analysisState;

  const errorCount    = status === 'success' && result ? result.diagnostics.filter(d => d.severity === 'error').length : 0;
  const warningCount  = status === 'success' && result ? result.diagnostics.filter(d => d.severity === 'warning').length : 0;
  const verifiedCount = status === 'success' && result ? result.traceability.filter(t => t.status === 'PASSED').length : 0;

  const analysisLabel = () => {
    if (status === 'loading') return 'Running…';
    if (status === 'success') return 'Complete';
    if (status === 'error')   return 'Failed';
    return 'Idle';
  };

  const isOnline = backendOnline && status !== 'error';

  return (
    <footer className="h-7 bg-[#080B0C] border-t border-slate-800/60 flex items-center justify-between px-4 text-[10px] font-mono select-none z-30 flex-shrink-0 no-print">
      {/* Left cluster */}
      <div className="flex items-center gap-5">
        <div className="flex items-center gap-1.5">
          <Server className={`w-3 h-3 ${isOnline ? 'text-emerald-500' : 'text-rose-500'}`} />
          <span className={isOnline ? 'text-emerald-500' : 'text-rose-400'}>
            {isOnline ? 'Ready' : 'Offline'}
          </span>
        </div>

        <div className="h-3 w-px bg-slate-800/60" />

        <div className="flex items-center gap-1.5">
          <Activity className={`w-3 h-3 ${status === 'loading' ? 'text-cyan-400 animate-pulse' : 'text-slate-700'}`} />
          <span className={
            status === 'loading' ? 'text-cyan-400'
            : status === 'success' ? 'text-emerald-500'
            : status === 'error' ? 'text-rose-400'
            : 'text-slate-700'
          }>{analysisLabel()}</span>
        </div>

        <div className="h-3 w-px bg-slate-800/60" />

        <div className="flex items-center gap-3 text-slate-700">
          <span className={inputStatus.hasRTL ? 'text-emerald-600' : ''}>RTL</span>
          <span className={inputStatus.hasSpecification ? 'text-emerald-600' : ''}>SPEC</span>
          <span className={inputStatus.hasTestbench ? 'text-emerald-600' : ''}>TB</span>
          <span className={inputStatus.hasWaveform ? 'text-emerald-600' : ''}>VCD</span>
        </div>
      </div>

      {/* Right cluster */}
      <div className="flex items-center gap-4">
        <div className={`flex items-center gap-1 ${errorCount > 0 ? 'text-rose-400' : 'text-slate-700'}`}>
          <AlertCircle className="w-3 h-3" />
          <span className="tabular-nums">{status === 'success' ? errorCount : '—'}</span>
        </div>
        <div className={`flex items-center gap-1 ${warningCount > 0 ? 'text-amber-400' : 'text-slate-700'}`}>
          <AlertTriangle className="w-3 h-3" />
          <span className="tabular-nums">{status === 'success' ? warningCount : '—'}</span>
        </div>
        <div className={`flex items-center gap-1 ${verifiedCount > 0 ? 'text-emerald-500' : 'text-slate-700'}`}>
          <CheckCircle className="w-3 h-3" />
          <span className="tabular-nums">{status === 'success' ? verifiedCount : '—'}</span>
        </div>
      </div>
    </footer>
  );
}
