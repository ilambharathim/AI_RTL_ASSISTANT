import { Sparkles, CheckCircle2 } from 'lucide-react';
import type { AIExplanation } from '../../types/api';

interface AIInsightSummaryProps {
  explanation?: AIExplanation;
}

export function AIInsightSummary({ explanation }: AIInsightSummaryProps) {
  if (!explanation || !explanation.summary) {
    return null;
  }

  return (
    <div className="p-5 rounded-xl border border-cyan-900/30 bg-cyan-950/10 space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-cyan-400" />
          <h3 className="text-xs font-semibold text-cyan-300 uppercase tracking-wider">AI Grounded Verification Reasoning</h3>
        </div>

        {explanation.confidence_score !== undefined && (
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-cyan-900/30 border border-cyan-800/50 text-cyan-400 font-mono text-xs font-semibold">
            <CheckCircle2 className="w-3.5 h-3.5" />
            Grounded confidence: {explanation.confidence_score}%
          </div>
        )}
      </div>

      <p className="text-slate-300 text-sm leading-relaxed font-sans bg-slate-950/50 p-4 rounded border border-slate-800/80">
        {explanation.summary}
      </p>

      {explanation.findings && explanation.findings.length > 0 && (
        <div className="space-y-2.5 pt-2">
          <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block font-mono">Detailed AI Findings</span>
          {explanation.findings.map((finding, idx) => (
            <div key={idx} className="p-3 rounded border border-slate-800 bg-[#0B0F10] space-y-1.5 font-mono text-xs">
              <div className="flex items-center justify-between text-slate-400">
                <span className="font-bold text-cyan-400 px-1.5 py-0.5 rounded bg-cyan-900/20 border border-cyan-800/40">
                  {finding.code}
                </span>
                {finding.location && (
                  <span className="text-slate-500 text-[10px]">{finding.location}</span>
                )}
              </div>
              <p className="text-slate-300 font-sans text-xs pt-1">{finding.explanation}</p>
              {finding.suggested_fix && (
                <p className="text-emerald-400 font-sans text-xs pt-1 border-t border-slate-800/60 mt-1">
                  <span className="font-bold">Recommended fix:</span> {finding.suggested_fix}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
