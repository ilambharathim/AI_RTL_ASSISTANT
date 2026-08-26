import { useState } from 'react';
import { ShieldCheck } from 'lucide-react';
import { RequirementTraceCard } from './RequirementTraceCard';
import type { TraceabilityLink, Diagnostic } from '../../types/api';

export type TraceFilter = 'all' | 'PASSED' | 'FAILED';

interface TraceabilityExplorerProps {
  traceability?: TraceabilityLink[];
  diagnostics?: Diagnostic[];
}

export function TraceabilityExplorer({ traceability = [], diagnostics = [] }: TraceabilityExplorerProps) {
  const [filter, setFilter] = useState<TraceFilter>('all');
  const [selectedReqId, setSelectedReqId] = useState<string | null>(null);

  if (!traceability || traceability.length === 0) {
    return (
      <div className="p-5 rounded-xl border border-slate-800 bg-[#0B0F10] space-y-2">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-slate-500" />
          <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Specification Traceability</h3>
        </div>
        <p className="text-xs text-slate-500 font-mono">No requirement verification yet. Run verification to inspect specification traceability.</p>
      </div>
    );
  }

  const totalCount = traceability.length;
  const passedCount = traceability.filter(t => t.status === 'PASSED').length;
  const failedCount = traceability.filter(t => t.status === 'FAILED').length;

  const filteredTrace = traceability.filter(t => {
    if (filter === 'PASSED') return t.status === 'PASSED';
    if (filter === 'FAILED') return t.status === 'FAILED';
    return true;
  });

  return (
    <div className="p-5 rounded-xl border border-slate-800 bg-[#0B0F10] space-y-4">
      {/* Header and Counts */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-cyan-400" />
          <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Specification Traceability</h3>
        </div>

        <div className="flex items-center gap-4 font-mono text-xs">
          <span className="text-slate-400">Total: <strong className="text-slate-200">{totalCount}</strong></span>
          <span className="text-emerald-400 font-semibold">{passedCount} passed</span>
          {failedCount > 0 && <span className="text-rose-400 font-semibold">{failedCount} failed</span>}
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center gap-1.5 bg-slate-900/60 p-1 rounded-lg border border-slate-800 text-xs font-mono w-fit">
        <button
          onClick={() => setFilter('all')}
          className={`px-3 py-1 rounded transition ${
            filter === 'all'
              ? 'bg-cyan-900/40 text-cyan-400 border border-cyan-800/50 font-bold'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          All ({totalCount})
        </button>
        <button
          onClick={() => setFilter('PASSED')}
          className={`px-3 py-1 rounded transition ${
            filter === 'PASSED'
              ? 'bg-emerald-900/40 text-emerald-400 border border-emerald-800/50 font-bold'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Passed ({passedCount})
        </button>
        <button
          onClick={() => setFilter('FAILED')}
          className={`px-3 py-1 rounded transition ${
            filter === 'FAILED'
              ? 'bg-rose-900/40 text-rose-400 border border-rose-800/50 font-bold'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Failed ({failedCount})
        </button>
      </div>

      {/* Requirement Cards List */}
      <div className="space-y-3 pt-1">
        {filteredTrace.map((item, idx) => {
          // Link related diagnostic if RIVA6002 or if message mentions requirement ID / signal name
          const relatedDiag = diagnostics.find(
            d => d.code === 'RIVA6002' ||
                 d.message?.includes(item.requirement_id) ||
                 (item.signal_name && d.message?.includes(item.signal_name))
          );

          return (
            <RequirementTraceCard
              key={`${item.requirement_id}-${idx}`}
              item={item}
              isSelected={selectedReqId === item.requirement_id}
              onSelect={() => setSelectedReqId(
                selectedReqId === item.requirement_id ? null : item.requirement_id
              )}
              relatedDiagnostic={item.status === 'FAILED' ? relatedDiag : undefined}
            />
          );
        })}
      </div>
    </div>
  );
}
