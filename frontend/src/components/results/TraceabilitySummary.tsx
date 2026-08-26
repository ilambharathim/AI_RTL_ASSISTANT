import { ShieldCheck, CheckCircle2, XCircle } from 'lucide-react';
import type { TraceabilityLink } from '../../types/api';

interface TraceabilitySummaryProps {
  traceability: TraceabilityLink[];
}

export function TraceabilitySummary({ traceability }: TraceabilitySummaryProps) {
  if (!traceability || traceability.length === 0) {
    return null;
  }

  const passedCount = traceability.filter(t => t.status === 'PASSED').length;
  const failedCount = traceability.filter(t => t.status === 'FAILED').length;

  return (
    <div className="p-5 rounded-xl border border-slate-800 bg-[#0B0F10] space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-cyan-400" />
          <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Specification Traceability</h3>
        </div>
        <div className="flex items-center gap-3 text-xs font-mono">
          <span className="text-emerald-400">{passedCount} passed</span>
          {failedCount > 0 && <span className="text-rose-400">{failedCount} failed</span>}
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left font-mono text-xs">
          <thead>
            <tr className="text-[10px] text-slate-500 uppercase border-b border-slate-800">
              <th className="pb-2.5 pr-4">Requirement ID</th>
              <th className="pb-2.5 pr-4">Target Signal</th>
              <th className="pb-2.5 pr-4">Expected</th>
              <th className="pb-2.5 pr-4">Actual Result</th>
              <th className="pb-2.5 text-right">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {traceability.map((item, idx) => {
              const isPassed = item.status === 'PASSED';

              return (
                <tr key={idx} className="hover:bg-slate-900/40 transition">
                  <td className="py-3 pr-4 font-bold text-cyan-400">{item.requirement_id}</td>
                  <td className="py-3 pr-4 text-slate-200">{item.signal_name || '—'}</td>
                  <td className="py-3 pr-4 text-slate-400">{item.expected || '—'}</td>
                  <td className="py-3 pr-4 text-slate-400">{item.actual || '—'}</td>
                  <td className="py-3 text-right">
                    {isPassed ? (
                      <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded border bg-emerald-900/30 text-emerald-400 border-emerald-800/50 text-[10px] font-bold">
                        <CheckCircle2 className="w-3 h-3" />
                        PASSED
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded border bg-rose-900/30 text-rose-400 border-rose-800/50 text-[10px] font-bold">
                        <XCircle className="w-3 h-3" />
                        FAILED
                      </span>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
