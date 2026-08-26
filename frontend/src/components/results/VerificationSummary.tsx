import { CheckCircle2, AlertCircle, AlertTriangle, ShieldCheck } from 'lucide-react';
import type { AnalyzeResponse } from '../../types/api';

interface VerificationSummaryProps {
  result: AnalyzeResponse;
}

export function VerificationSummary({ result }: VerificationSummaryProps) {
  const errorCount   = result.diagnostics.filter(d => d.severity === 'error').length;
  const warningCount = result.diagnostics.filter(d => d.severity === 'warning').length;
  const reqCount     = result.traceability.length;
  const reqPassed    = result.traceability.filter(t => t.status === 'PASSED').length;
  const waveformAvailable = result.waveform?.status === 'success';

  let statusText  = 'VERIFICATION PASSED';
  let statusColor = 'emerald' as 'emerald' | 'rose' | 'amber';

  if (errorCount > 0) {
    statusText  = 'VERIFICATION FAILED';
    statusColor = 'rose';
  } else if (warningCount > 0) {
    statusText  = 'PASSED WITH WARNINGS';
    statusColor = 'amber';
  }

  const StatusIcon = statusColor === 'emerald' ? CheckCircle2
                   : statusColor === 'rose'    ? AlertCircle
                   : AlertTriangle;

  const colorMap = {
    emerald: {
      card:   'bg-emerald-950/10 border-emerald-900/30',
      icon:   'bg-emerald-900/25 border-emerald-800/50 text-emerald-400',
      label:  'text-emerald-400',
    },
    rose: {
      card:   'bg-rose-950/10 border-rose-900/30',
      icon:   'bg-rose-900/25 border-rose-800/50 text-rose-400',
      label:  'text-rose-400',
    },
    amber: {
      card:   'bg-amber-950/10 border-amber-900/30',
      icon:   'bg-amber-900/25 border-amber-800/50 text-amber-400',
      label:  'text-amber-400',
    },
  };
  const c = colorMap[statusColor];

  return (
    <div className={`p-5 rounded-xl border shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-5 ${c.card}`}>
      {/* Status block */}
      <div className="flex items-center gap-4">
        <div className={`w-11 h-11 rounded-full border flex items-center justify-center flex-shrink-0 ${c.icon}`}>
          <StatusIcon className="w-5 h-5" />
        </div>
        <div>
          <span className={`text-[11px] font-mono font-semibold tracking-widest uppercase ${c.label}`}>
            {statusText}
          </span>
          <div className="flex items-center gap-2 mt-0.5">
            <ShieldCheck className="w-3.5 h-3.5 text-slate-600" />
            <span className="text-base font-bold text-slate-100">
              Top module: <span className="text-cyan-400 font-mono">{result.top_module || '—'}</span>
            </span>
          </div>
        </div>
      </div>

      {/* Metrics strip */}
      <div className="flex items-center gap-5 font-mono text-xs text-slate-400 sm:border-l border-slate-800/80 sm:pl-5">
        <div className="text-center">
          <span className="text-[10px] text-slate-600 uppercase tracking-wider block mb-0.5">Errors</span>
          <span className={`text-lg font-bold leading-none tabular-nums ${errorCount > 0 ? 'text-rose-400' : 'text-slate-400'}`}>{errorCount}</span>
        </div>
        <div className="text-center">
          <span className="text-[10px] text-slate-600 uppercase tracking-wider block mb-0.5">Warnings</span>
          <span className={`text-lg font-bold leading-none tabular-nums ${warningCount > 0 ? 'text-amber-400' : 'text-slate-400'}`}>{warningCount}</span>
        </div>
        <div className="h-8 w-px bg-slate-800/60 hidden sm:block" />
        <div className="text-center">
          <span className="text-[10px] text-slate-600 uppercase tracking-wider block mb-0.5">Reqs</span>
          <span className="text-lg font-bold leading-none tabular-nums text-cyan-400">{reqPassed}<span className="text-slate-600 text-sm">/{reqCount}</span></span>
        </div>
        <div className="text-center">
          <span className="text-[10px] text-slate-600 uppercase tracking-wider block mb-0.5">Waveform</span>
          <span className={`text-sm font-bold leading-none ${waveformAvailable ? 'text-emerald-400' : 'text-slate-600'}`}>
            {waveformAvailable ? 'OK' : 'N/A'}
          </span>
        </div>
      </div>
    </div>
  );
}
