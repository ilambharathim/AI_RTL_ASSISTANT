import { CheckCircle2, XCircle, AlertCircle } from 'lucide-react';
import type { TraceabilityLink, Diagnostic } from '../../types/api';

interface RequirementTraceCardProps {
  item: TraceabilityLink;
  isSelected: boolean;
  onSelect: () => void;
  relatedDiagnostic?: Diagnostic;
}

export function RequirementTraceCard({ item, isSelected, onSelect, relatedDiagnostic }: RequirementTraceCardProps) {
  const isPassed = item.status === 'PASSED';

  return (
    <div
      onClick={onSelect}
      className={`p-4 rounded-xl border transition-all duration-200 cursor-pointer select-none ${
        isSelected
          ? 'border-cyan-500 bg-cyan-950/20 shadow-[0_0_20px_rgba(34,211,238,0.1)]'
          : isPassed
          ? 'border-slate-800 hover:border-slate-700 bg-[#0B0F10]'
          : 'border-rose-900/40 hover:border-rose-800/60 bg-rose-950/10'
      }`}
    >
      <div className="flex items-center justify-between font-mono">
        <div className="flex items-center gap-2">
          <span className="font-bold text-sm text-cyan-400">{item.requirement_id}</span>
          {item.signal_name && (
            <span className="text-xs text-slate-400 border-l border-slate-800 pl-2">
              Signal: <span className="text-slate-200 font-semibold">{item.signal_name}</span>
            </span>
          )}
        </div>

        <div>
          {isPassed ? (
            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded border bg-emerald-900/30 text-emerald-400 border-emerald-800/50 text-[10px] font-bold">
              <CheckCircle2 className="w-3 h-3" />
              PASSED
            </span>
          ) : (
            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded border bg-rose-900/30 text-rose-400 border-rose-800/50 text-[10px] font-bold">
              <XCircle className="w-3 h-3" />
              FAILED
            </span>
          )}
        </div>
      </div>

      <div className="mt-3 grid grid-cols-1 md:grid-cols-2 gap-3 text-xs font-mono">
        <div className="bg-slate-950/60 p-2.5 rounded border border-slate-800/80">
          <span className="text-[10px] text-slate-500 uppercase tracking-wider block mb-0.5">Expected</span>
          <span className="text-slate-300">{item.expected || '—'}</span>
        </div>
        <div className="bg-slate-950/60 p-2.5 rounded border border-slate-800/80">
          <span className="text-[10px] text-slate-500 uppercase tracking-wider block mb-0.5">Actual Result</span>
          <span className={isPassed ? 'text-emerald-400' : 'text-rose-400'}>{item.actual || '—'}</span>
        </div>
      </div>

      {/* Connection to related diagnostic if present */}
      {relatedDiagnostic && (
        <div className="mt-3 p-2.5 rounded bg-rose-950/30 border border-rose-900/50 text-xs font-mono flex items-center justify-between text-rose-300">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-3.5 h-3.5 text-rose-400 flex-shrink-0" />
            <span>Related Diagnostic: <strong className="text-rose-200">{relatedDiagnostic.code}</strong></span>
          </div>
          <span className="text-[10px] text-rose-400/80 truncate max-w-xs">{relatedDiagnostic.message}</span>
        </div>
      )}
    </div>
  );
}
