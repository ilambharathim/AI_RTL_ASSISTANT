import { useState } from 'react';
import { Wrench, MapPin, Copy, Check, Sparkles, ArrowLeft, Info } from 'lucide-react';
import type { Diagnostic, AIFinding } from '../../types/api';

interface RepairSuggestionCardProps {
  diagnostic: Diagnostic;
  aiFinding?: AIFinding;
  onGoToEditor?: () => void;
}

export function RepairSuggestionCard({ diagnostic, aiFinding, onGoToEditor }: RepairSuggestionCardProps) {
  const [copied, setCopied] = useState(false);

  const isError = diagnostic.severity === 'error';
  const isWarning = diagnostic.severity === 'warning';

  const badgeStyle = isError
    ? 'bg-rose-900/30 text-rose-400 border-rose-800/60'
    : isWarning
    ? 'bg-amber-900/30 text-amber-400 border-amber-800/60'
    : 'bg-cyan-900/30 text-cyan-400 border-cyan-800/60';

  const suggestionText = diagnostic.suggestion || aiFinding?.suggested_fix || 'Review SystemVerilog signal width and logic assignment';

  const handleCopy = () => {
    navigator.clipboard.writeText(suggestionText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="p-5 rounded-xl border border-slate-800 bg-[#0B0F10] space-y-4 font-mono text-xs shadow-lg">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2.5">
          <Wrench className="w-4 h-4 text-cyan-400" />
          <span className="font-bold text-sm text-slate-200">Guided Repair</span>
          <span className={`px-2 py-0.5 rounded border text-[10px] font-bold ${badgeStyle}`}>
            {diagnostic.code}
          </span>
        </div>

        {diagnostic.location && (
          <span className="text-[11px] text-slate-500 flex items-center gap-1">
            <MapPin className="w-3 h-3 text-slate-600" />
            {diagnostic.location}
          </span>
        )}
      </div>

      {/* Problem Description */}
      <div className="bg-slate-950/60 p-3.5 rounded border border-slate-800/80 space-y-1">
        <span className="text-[10px] text-slate-500 uppercase tracking-wider block font-semibold">Detected Problem</span>
        <p className="text-slate-200 text-sm font-sans leading-relaxed">{diagnostic.message}</p>
      </div>

      {/* AI Grounded Explanation if present */}
      {aiFinding?.explanation && (
        <div className="bg-cyan-950/20 p-3.5 rounded border border-cyan-900/40 space-y-1">
          <span className="text-[10px] text-cyan-400 uppercase tracking-wider font-semibold flex items-center gap-1">
            <Sparkles className="w-3 h-3" />
            Grounded Reasoning
          </span>
          <p className="text-slate-300 text-xs font-sans leading-relaxed">{aiFinding.explanation}</p>
        </div>
      )}

      {/* Recommended Fix Box */}
      <div className="bg-emerald-950/20 p-3.5 rounded border border-emerald-900/40 space-y-1">
        <span className="text-[10px] text-emerald-400 uppercase tracking-wider font-semibold flex items-center gap-1">
          <Wrench className="w-3 h-3" />
          Recommended Fix
        </span>
        <p className="text-emerald-300 text-xs font-sans leading-relaxed">{suggestionText}</p>
      </div>

      {/* Code Patch / Replacement Preview State Notice */}
      <div className="bg-slate-950/40 p-3 rounded border border-slate-800/80 text-[11px] text-slate-500 flex items-start gap-2">
        <Info className="w-4 h-4 text-slate-600 flex-shrink-0 mt-0.5" />
        <span>
          Automated code patch preview is not available for this diagnostic. Engineer review required before applying changes in the RTL editor.
        </span>
      </div>

      {/* Action Toolbar */}
      <div className="pt-2 flex items-center justify-between gap-3 border-t border-slate-800">
        <button
          type="button"
          onClick={handleCopy}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 hover:text-cyan-400 transition"
        >
          {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5 text-slate-400" />}
          <span>{copied ? 'Copied to Clipboard!' : 'Copy Suggested Fix'}</span>
        </button>

        {onGoToEditor && (
          <button
            type="button"
            onClick={onGoToEditor}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-cyan-900/40 hover:bg-cyan-900/60 border border-cyan-800/60 text-cyan-400 transition font-semibold"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Return to RTL Editor</span>
          </button>
        )}
      </div>
    </div>
  );
}
