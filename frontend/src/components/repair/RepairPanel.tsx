import { useState } from 'react';
import { Wrench, CheckCircle2 } from 'lucide-react';
import { RepairSuggestionCard } from './RepairSuggestionCard';
import type { Diagnostic, AIExplanation } from '../../types/api';

interface RepairPanelProps {
  diagnostics?: Diagnostic[];
  explanation?: AIExplanation;
  selectedCode?: string | null;
  onNavigateToEditor?: () => void;
}

export function RepairPanel({ diagnostics = [], explanation, selectedCode, onNavigateToEditor }: RepairPanelProps) {
  const [userSelectedCode, setUserSelectedCode] = useState<string | null>(null);

  // Derive active code: preference to user click, then prop, then first diagnostic
  const activeCode = (userSelectedCode && diagnostics.some(d => d.code === userSelectedCode))
    ? userSelectedCode
    : (selectedCode && diagnostics.some(d => d.code === selectedCode))
    ? selectedCode
    : (diagnostics[0]?.code ?? null);

  // Clean Design Case
  if (!diagnostics || diagnostics.length === 0) {
    return (
      <div className="p-6 rounded-xl border border-emerald-900/40 bg-emerald-950/10 text-center space-y-3 font-mono text-xs">
        <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-emerald-900/30 text-emerald-400 border border-emerald-700/50">
          <CheckCircle2 className="w-6 h-6" />
        </div>
        <h3 className="text-sm font-bold text-emerald-400">NO REPAIRS REQUIRED</h3>
        <p className="text-slate-400 font-sans max-w-md mx-auto">
          The SystemVerilog RTL design contains no detected diagnostic violations. All static and semantic checks passed successfully.
        </p>
      </div>
    );
  }

  // Find active diagnostic object and matching AI finding
  const activeDiagnostic = diagnostics.find(d => d.code === activeCode) || diagnostics[0];
  const activeAiFinding = explanation?.findings?.find(
    f => f.code?.toUpperCase() === activeDiagnostic.code?.toUpperCase()
  );

  return (
    <div className="p-5 rounded-xl border border-slate-800 bg-[#0B0F10] space-y-5">
      {/* Panel Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <Wrench className="w-4 h-4 text-cyan-400" />
          <h3 className="text-xs font-semibold text-slate-200 uppercase tracking-wider">Guided Repair Center</h3>
        </div>
        <span className="text-[10px] font-mono text-slate-500">
          {diagnostics.length} diagnostic violation{diagnostics.length !== 1 ? 's' : ''} requiring review
        </span>
      </div>

      {/* Diagnostic Selector Tabs (if multiple diagnostics exist) */}
      {diagnostics.length > 1 && (
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 font-mono text-xs">
          {diagnostics.map((d, idx) => {
            const isSelected = d.code === activeDiagnostic.code;
            const isError = d.severity === 'error';

            return (
              <button
                key={`${d.code}-${idx}`}
                type="button"
                onClick={() => setUserSelectedCode(d.code)}
                className={`px-3 py-1 rounded border text-xs transition flex items-center gap-2 whitespace-nowrap ${
                  isSelected
                    ? 'bg-cyan-900/40 text-cyan-400 border-cyan-800 font-bold'
                    : isError
                    ? 'bg-slate-900/60 text-rose-400 border-rose-900/40 hover:bg-slate-900'
                    : 'bg-slate-900/60 text-slate-400 border-slate-800 hover:text-slate-200'
                }`}
              >
                <span>{d.code}</span>
                <span className={`w-1.5 h-1.5 rounded-full ${isError ? 'bg-rose-400' : 'bg-amber-400'}`} />
              </button>
            );
          })}
        </div>
      )}

      {/* Active Repair Card */}
      {activeDiagnostic && (
        <RepairSuggestionCard
          diagnostic={activeDiagnostic}
          aiFinding={activeAiFinding}
          onGoToEditor={onNavigateToEditor}
        />
      )}
    </div>
  );
}
