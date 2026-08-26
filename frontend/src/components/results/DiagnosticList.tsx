import { DiagnosticCard } from './DiagnosticCard';
import type { DiagnosticFilter } from './DiagnosticOverview';
import type { Diagnostic, AIExplanation } from '../../types/api';

interface DiagnosticListProps {
  diagnostics: Diagnostic[];
  explanation?: AIExplanation;
  activeFilter: DiagnosticFilter;
  onViewRepair?: (code: string) => void;
}

export function DiagnosticList({ diagnostics, explanation, activeFilter, onViewRepair }: DiagnosticListProps) {
  const filteredDiagnostics = diagnostics.filter(d => {
    if (activeFilter === 'error') return d.severity === 'error';
    if (activeFilter === 'warning') return d.severity === 'warning';
    return true;
  });

  if (diagnostics.length === 0) {
    return (
      <div className="p-8 rounded-xl border border-emerald-900/40 bg-emerald-950/10 text-center space-y-2 font-mono text-xs">
        <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-emerald-900/30 text-emerald-400 border border-emerald-700/50 mb-1">
          ✓
        </div>
        <h3 className="text-base font-bold text-emerald-400 font-sans">VERIFICATION PASSED</h3>
        <p className="text-xs text-slate-400 max-w-md mx-auto font-sans">
          No diagnostic violations detected. Your SystemVerilog RTL conforms to the verified static and semantic rules.
        </p>
      </div>
    );
  }

  if (filteredDiagnostics.length === 0) {
    return (
      <div className="p-6 rounded-xl border border-slate-800 bg-[#0B0F10] text-center text-slate-500 text-xs font-mono">
        No diagnostics match the selected filter ({activeFilter}).
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {filteredDiagnostics.map((diag, idx) => {
        const aiFinding = explanation?.findings?.find(
          f => f.code?.toUpperCase() === diag.code?.toUpperCase()
        );

        return (
          <DiagnosticCard
            key={`${diag.code}-${diag.location}-${idx}`}
            diagnostic={diag}
            aiFinding={aiFinding}
            defaultExpanded={diag.severity === 'error'}
            onViewRepair={onViewRepair}
          />
        );
      })}
    </div>
  );
}
