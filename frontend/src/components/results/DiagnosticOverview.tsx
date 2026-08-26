import { AlertCircle, AlertTriangle } from 'lucide-react';
import type { Diagnostic } from '../../types/api';

export type DiagnosticFilter = 'all' | 'error' | 'warning';

interface DiagnosticOverviewProps {
  diagnostics: Diagnostic[];
  activeFilter: DiagnosticFilter;
  onFilterChange: (filter: DiagnosticFilter) => void;
}

export function DiagnosticOverview({ diagnostics, activeFilter, onFilterChange }: DiagnosticOverviewProps) {
  const errorCount   = diagnostics.filter(d => d.severity === 'error').length;
  const warningCount = diagnostics.filter(d => d.severity === 'warning').length;
  const totalCount   = diagnostics.length;

  const filters: { key: DiagnosticFilter; label: string; count: number; activeClass: string }[] = [
    { key: 'all',     label: 'All',      count: totalCount,   activeClass: 'bg-cyan-900/40 text-cyan-400 border border-cyan-800/50' },
    { key: 'error',   label: 'Errors',   count: errorCount,   activeClass: 'bg-rose-900/40 text-rose-400 border border-rose-800/50' },
    { key: 'warning', label: 'Warnings', count: warningCount, activeClass: 'bg-amber-900/40 text-amber-400 border border-amber-800/50' },
  ];

  return (
    <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-4 rounded-xl border border-slate-800/80 bg-[#0B0F10]">
      {/* Counts */}
      <div className="flex items-center gap-5 font-mono">
        <div className="text-center">
          <span className="text-[10px] text-slate-600 uppercase tracking-wider block mb-0.5">Total</span>
          <span className="text-lg font-bold text-slate-200 tabular-nums">{totalCount}</span>
        </div>
        <div className="h-7 w-px bg-slate-800/60" />
        <div className="flex items-center gap-1.5 text-center">
          <AlertCircle className={`w-3.5 h-3.5 ${errorCount > 0 ? 'text-rose-400' : 'text-slate-700'}`} />
          <span className={`text-lg font-bold tabular-nums ${errorCount > 0 ? 'text-rose-400' : 'text-slate-600'}`}>{errorCount}</span>
        </div>
        <div className="flex items-center gap-1.5 text-center">
          <AlertTriangle className={`w-3.5 h-3.5 ${warningCount > 0 ? 'text-amber-400' : 'text-slate-700'}`} />
          <span className={`text-lg font-bold tabular-nums ${warningCount > 0 ? 'text-amber-400' : 'text-slate-600'}`}>{warningCount}</span>
        </div>
      </div>

      {/* Filter tabs */}
      <div className="flex items-center gap-1 bg-slate-950/60 p-1 rounded-lg border border-slate-800/60 text-[11px] font-mono">
        {filters.map(f => (
          <button
            key={f.key}
            type="button"
            onClick={() => onFilterChange(f.key)}
            className={`px-3 py-1.5 rounded-md transition-all duration-150 font-semibold focus-visible:ring-2 focus-visible:ring-cyan-500/50 ${
              activeFilter === f.key
                ? f.activeClass
                : 'text-slate-500 hover:text-slate-300 border border-transparent'
            }`}
          >
            {f.label} ({f.count})
          </button>
        ))}
      </div>
    </div>
  );
}
