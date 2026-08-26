import { useState } from 'react';
import { ChevronDown, ChevronRight, MapPin, Wrench, Sparkles, ArrowRight } from 'lucide-react';
import type { Diagnostic, AIFinding } from '../../types/api';

interface DiagnosticCardProps {
  diagnostic: Diagnostic;
  aiFinding?: AIFinding;
  defaultExpanded?: boolean;
  onViewRepair?: (code: string) => void;
}

export function DiagnosticCard({ diagnostic, aiFinding, defaultExpanded = true, onViewRepair }: DiagnosticCardProps) {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);

  const isError = diagnostic.severity === 'error';
  const isWarning = diagnostic.severity === 'warning';

  const badgeStyle = isError
    ? 'bg-rose-900/30 text-rose-400 border-rose-800/60'
    : isWarning
    ? 'bg-amber-900/30 text-amber-400 border-amber-800/60'
    : 'bg-cyan-900/30 text-cyan-400 border-cyan-800/60';

  const cardBorderStyle = isError
    ? 'border-rose-900/30 hover:border-rose-800/60 bg-rose-950/10'
    : isWarning
    ? 'border-amber-900/30 hover:border-amber-800/60 bg-amber-950/10'
    : 'border-slate-800 hover:border-slate-700 bg-[#0B0F10]';

  return (
    <div className={`rounded-xl border transition-all duration-200 overflow-hidden ${cardBorderStyle}`}>
      {/* Header Bar */}
      <div
        onClick={() => setIsExpanded(!isExpanded)}
        className="flex items-center justify-between p-4 cursor-pointer select-none"
      >
        <div className="flex items-center gap-3 min-w-0">
          <button className="text-slate-500 hover:text-slate-300">
            {isExpanded ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
          </button>

          <span className={`px-2 py-0.5 rounded border text-xs font-mono font-bold tracking-wider ${badgeStyle}`}>
            {diagnostic.code}
          </span>

          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400 border-l border-slate-800 pl-3">
            {diagnostic.category}
          </span>

          <span className="text-xs font-mono text-slate-300 truncate ml-2">
            {diagnostic.message}
          </span>
        </div>

        <div className="flex items-center gap-3 flex-shrink-0 ml-4">
          {diagnostic.location && (
            <span className="text-[11px] font-mono text-slate-500 flex items-center gap-1">
              <MapPin className="w-3 h-3 text-slate-600" />
              {diagnostic.location}
            </span>
          )}
          <span className={`text-[10px] font-mono uppercase font-bold px-2 py-0.5 rounded border ${badgeStyle}`}>
            {diagnostic.severity}
          </span>
        </div>
      </div>

      {/* Expanded Content Details */}
      {isExpanded && (
        <div className="px-4 pb-4 pt-1 border-t border-slate-800/60 space-y-3 font-mono text-xs">

          {/* Main Diagnostic Message */}
          <div className="bg-slate-950/60 p-3 rounded border border-slate-800/80">
            <span className="text-[10px] text-slate-500 uppercase tracking-wider block mb-1">Diagnostic Message</span>
            <p className="text-slate-200 text-sm font-sans leading-relaxed">{diagnostic.message}</p>
          </div>

          {/* Backend Fix Suggestion */}
          {diagnostic.suggestion && (
            <div className="bg-emerald-950/20 border border-emerald-900/40 p-3 rounded">
              <span className="text-[10px] text-emerald-400 uppercase tracking-wider font-semibold flex items-center gap-1 mb-1">
                <Wrench className="w-3 h-3" />
                Backend Recommendation
              </span>
              <p className="text-emerald-300 text-xs font-sans">{diagnostic.suggestion}</p>
            </div>
          )}

          {/* Grounded AI Explanation payload if present */}
          {aiFinding && (
            <div className="bg-cyan-950/20 border border-cyan-900/40 p-3 rounded">
              <span className="text-[10px] text-cyan-400 uppercase tracking-wider font-semibold flex items-center gap-1 mb-1">
                <Sparkles className="w-3 h-3" />
                Grounded AI Explanation
              </span>
              <p className="text-slate-300 text-xs font-sans leading-relaxed">{aiFinding.explanation}</p>
              {aiFinding.suggested_fix && aiFinding.suggested_fix !== diagnostic.suggestion && (
                <p className="text-cyan-300 text-xs font-sans mt-2 pt-2 border-t border-cyan-900/40">
                  <span className="font-semibold">AI Suggested Fix:</span> {aiFinding.suggested_fix}
                </p>
              )}
            </div>
          )}

          {/* Guided Repair Action Link */}
          {onViewRepair && (
            <div className="pt-1 flex justify-end">
              <button
                type="button"
                onClick={(e) => {
                  e.stopPropagation();
                  onViewRepair(diagnostic.code);
                }}
                className="flex items-center gap-1.5 px-3 py-1 rounded bg-slate-900 hover:bg-slate-800 border border-slate-700 text-cyan-400 hover:text-cyan-300 transition text-xs font-semibold"
              >
                <span>Guided Repair</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          )}

        </div>
      )}
    </div>
  );
}
