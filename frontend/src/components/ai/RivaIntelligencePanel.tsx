import { useState } from 'react';
import { Sparkles, CheckCircle2, ChevronDown, ChevronRight, ShieldCheck, MapPin, Wrench, AlertCircle } from 'lucide-react';
import type { AnalysisState } from '../../types/state';
import type { AIFinding, Diagnostic } from '../../types/api';

interface RivaIntelligencePanelProps {
  analysisState: AnalysisState;
  onSelectDiagnostic?: (code: string) => void;
}

export function RivaIntelligencePanel({ analysisState, onSelectDiagnostic }: RivaIntelligencePanelProps) {
  const { status, result, error } = analysisState;

  // 1. Idle / Pre-analysis State
  if (status === 'idle' || !result) {
    return (
      <div className="p-4 space-y-3 font-mono text-xs text-slate-400">
        <div className="flex items-center gap-2 text-cyan-400 font-bold border-b border-slate-800 pb-2">
          <Sparkles className="w-4 h-4" />
          <span>RIVA INTELLIGENCE</span>
        </div>
        <p className="text-slate-500 font-sans text-xs leading-relaxed">
          No verification evidence yet. Run verification to generate grounded design analysis and recommendations.
        </p>
      </div>
    );
  }

  // 2. Loading State
  if (status === 'loading') {
    return (
      <div className="p-4 space-y-3 font-mono text-xs">
        <div className="flex items-center gap-2 text-cyan-400 font-bold border-b border-slate-800 pb-2">
          <Sparkles className="w-4 h-4 animate-spin" />
          <span>RIVA INTELLIGENCE</span>
        </div>
        <p className="text-cyan-300 font-sans text-xs animate-pulse">
          Analyzing deterministic evidence...
        </p>
      </div>
    );
  }

  // 3. Analysis Error State
  if (status === 'error') {
    return (
      <div className="p-4 space-y-3 font-mono text-xs">
        <div className="flex items-center gap-2 text-rose-400 font-bold border-b border-slate-800 pb-2">
          <AlertCircle className="w-4 h-4" />
          <span>RIVA INTELLIGENCE</span>
        </div>
        <p className="text-rose-300 font-sans text-xs leading-relaxed">
          Analysis unavailable. {error || 'Failed to analyze design.'}
        </p>
      </div>
    );
  }

  const explanation = result.explanation;
  const diagnostics = result.diagnostics ?? [];
  const findings = explanation?.findings ?? [];
  const confidenceScore = explanation?.confidence_score ?? 95;
  const isClean = diagnostics.length === 0;

  return (
    <div className="p-4 space-y-4 font-mono text-xs">
      {/* Header & Confidence */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2 text-cyan-400 font-bold">
          <Sparkles className="w-4 h-4" />
          <span>RIVA INTELLIGENCE</span>
        </div>
        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-cyan-900/30 text-cyan-400 border border-cyan-800/50 text-[10px] font-bold">
          <CheckCircle2 className="w-3 h-3" />
          {confidenceScore}%
        </span>
      </div>

      {/* Clean Design Positive State */}
      {isClean ? (
        <div className="p-3.5 rounded-lg border border-emerald-900/40 bg-emerald-950/20 space-y-2">
          <div className="flex items-center gap-2 text-emerald-400 font-bold text-xs">
            <CheckCircle2 className="w-4 h-4" />
            <span>VERIFICATION GROUNDED</span>
          </div>
          <p className="text-slate-300 font-sans text-xs leading-relaxed">
            Design verified successfully. No deterministic violations require AI explanation.
          </p>
          <p className="text-[10px] text-slate-500 font-mono">
            Grounded confidence: {confidenceScore}%
          </p>
        </div>
      ) : (
        /* Summary Text */
        explanation?.summary && (
          <div className="bg-slate-950/60 p-3 rounded border border-slate-800/80 space-y-1">
            <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block">Grounded Summary</span>
            <p className="text-slate-300 font-sans text-xs leading-relaxed">{explanation.summary}</p>
          </div>
        )
      )}

      {/* Findings Breakdown */}
      {findings.length > 0 && (
        <div className="space-y-2 pt-1">
          <div className="flex items-center justify-between text-[10px] font-semibold text-slate-500 uppercase tracking-wider">
            <span>AI Findings ({findings.length})</span>
            <span>Grounded in Evidence</span>
          </div>

          <div className="space-y-2">
            {findings.map((finding, idx) => {
              const matchingDiag = diagnostics.find(
                d => d.code?.toUpperCase() === finding.code?.toUpperCase()
              );
              return (
                <AIFindingItemCard
                  key={`${finding.code}-${idx}`}
                  index={idx + 1}
                  finding={finding}
                  matchingDiag={matchingDiag}
                  onSelect={() => onSelectDiagnostic?.(finding.code)}
                />
              );
            })}
          </div>
        </div>
      )}

      {!isClean && findings.length === 0 && (
        <p className="text-slate-500 text-[11px] italic">No additional AI findings generated for this run.</p>
      )}
    </div>
  );
}

/* ── Individual AI Finding Item Card Component ── */
interface AIFindingItemCardProps {
  index: number;
  finding: AIFinding;
  matchingDiag?: Diagnostic;
  onSelect?: () => void;
}

function AIFindingItemCard({ index, finding, matchingDiag, onSelect }: AIFindingItemCardProps) {
  const [isExpanded, setIsExpanded] = useState(index === 1);

  const severity = matchingDiag?.severity ?? 'info';
  const isError = severity === 'error';
  const isWarning = severity === 'warning';

  const cardStyle = isError
    ? 'border-rose-900/40 bg-rose-950/10 hover:border-rose-800/60'
    : isWarning
    ? 'border-amber-900/40 bg-amber-950/10 hover:border-amber-800/60'
    : 'border-slate-800 bg-[#0B0F10] hover:border-slate-700';

  const badgeStyle = isError
    ? 'bg-rose-900/30 text-rose-400 border-rose-800/50'
    : isWarning
    ? 'bg-amber-900/30 text-amber-400 border-amber-800/50'
    : 'bg-cyan-900/30 text-cyan-400 border-cyan-800/50';

  return (
    <div className={`rounded-lg border transition-all duration-200 overflow-hidden font-mono text-xs ${cardStyle}`}>
      {/* Header Bar */}
      <div
        onClick={() => setIsExpanded(!isExpanded)}
        className="p-2.5 flex items-center justify-between cursor-pointer select-none"
      >
        <div className="flex items-center gap-2 min-w-0">
          <span className="text-slate-500 text-[10px] font-bold">{index}.</span>
          <span className={`px-1.5 py-0.5 rounded border text-[10px] font-bold ${badgeStyle}`}>
            {finding.code}
          </span>
          <span className="text-slate-300 font-sans text-xs truncate">
            {finding.explanation.slice(0, 45)}...
          </span>
        </div>

        <div className="flex items-center gap-2 flex-shrink-0 ml-2">
          {matchingDiag && (
            <span className={`text-[9px] uppercase font-bold px-1.5 py-0.5 rounded border ${badgeStyle}`}>
              {severity}
            </span>
          )}
          <button className="text-slate-500 hover:text-slate-300">
            {isExpanded ? <ChevronDown className="w-3.5 h-3.5" /> : <ChevronRight className="w-3.5 h-3.5" />}
          </button>
        </div>
      </div>

      {/* Expanded Details */}
      {isExpanded && (
        <div className="p-3 border-t border-slate-800/60 space-y-2.5 bg-slate-950/50">
          {/* Grounding Badge */}
          <div className="flex items-center justify-between text-[10px] text-slate-500">
            <span className="inline-flex items-center gap-1 text-cyan-400 font-semibold">
              <ShieldCheck className="w-3 h-3" />
              GROUNDED IN VERIFIED EVIDENCE
            </span>
            {finding.location && (
              <span className="flex items-center gap-1 text-slate-500 font-mono">
                <MapPin className="w-3 h-3 text-slate-600" />
                {finding.location}
              </span>
            )}
          </div>

          {/* Explanation Text */}
          <p className="text-slate-200 font-sans text-xs leading-relaxed">{finding.explanation}</p>

          {/* Recommended Fix */}
          {finding.suggested_fix && (
            <div className="bg-emerald-950/20 border border-emerald-900/40 p-2.5 rounded">
              <span className="text-[10px] text-emerald-400 font-semibold uppercase tracking-wider flex items-center gap-1 mb-1">
                <Wrench className="w-3 h-3" />
                Suggested Fix
              </span>
              <p className="text-emerald-300 font-sans text-xs">{finding.suggested_fix}</p>
            </div>
          )}

          {/* Link to Diagnostic Button */}
          {matchingDiag && (
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                onSelect?.();
              }}
              className="w-full py-1 rounded bg-slate-900 hover:bg-slate-800 border border-slate-800 text-[10px] font-mono text-cyan-400 hover:text-cyan-300 transition flex items-center justify-center gap-1.5"
            >
              Supported by Diagnostic <strong className="underline">{matchingDiag.code}</strong>
            </button>
          )}
        </div>
      )}
    </div>
  );
}
