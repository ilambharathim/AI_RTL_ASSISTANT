import { useState } from 'react';
import { Wrench, MapPin, Copy, Check, Sparkles, ArrowLeft, Code, Layers } from 'lucide-react';
import type { Diagnostic, AIFinding } from '../../types/api';

interface RepairSuggestionCardProps {
  diagnostic: Diagnostic;
  aiFinding?: AIFinding;
  onGoToEditor?: () => void;
}

export function RepairSuggestionCard({ diagnostic, aiFinding, onGoToEditor }: RepairSuggestionCardProps) {
  const [copied, setCopied] = useState(false);
  const [selectedOption, setSelectedOption] = useState<number>(0);

  const isError = diagnostic.severity === 'error';
  const isWarning = diagnostic.severity === 'warning';

  const badgeStyle = isError
    ? 'bg-rose-900/30 text-rose-400 border-rose-800/60'
    : isWarning
    ? 'bg-amber-900/30 text-amber-400 border-amber-800/60'
    : 'bg-cyan-900/30 text-cyan-400 border-cyan-800/60';

  const suggestionText = diagnostic.suggestion || aiFinding?.suggested_fix || 'Review SystemVerilog signal width and logic assignment';

  // Generate deterministic correction options based on diagnostic code
  const getCorrectionOptions = () => {
    switch (diagnostic.code) {
      case 'RIVA3001':
        return [
          {
            title: 'Option A: Explicit Bit-Slice Selection',
            description: 'Truncate source bits explicitly using a bit slice to fit target signal width.',
            before: 'output logic [3:0] y;\nassign y = a;',
            after: 'output logic [3:0] y;\nassign y = a[3:0];',
          },
          {
            title: 'Option B: Align Output Port Width',
            description: 'Expand target output port width declaration to match 8-bit source expression.',
            before: 'output logic [3:0] y;\nassign y = a;',
            after: 'output logic [7:0] y;\nassign y = a;',
          },
        ];

      case 'RIVA3002':
        return [
          {
            title: 'Option A: Explicit Unsigned Cast',
            description: 'Cast signed expression with $unsigned() before logic assignment.',
            before: 'output logic [7:0] y;\nassign y = a; // a is signed',
            after: 'output logic [7:0] y;\nassign y = $unsigned(a);',
          },
          {
            title: 'Option B: Align Target Signedness',
            description: 'Declare output net as signed to match source operand signedness.',
            before: 'output logic [7:0] y;\nassign y = a;',
            after: 'output logic signed [7:0] y;\nassign y = a;',
          },
        ];

      case 'RIVA1001':
        return [
          {
            title: 'Option A: Add Missing Signal Declaration',
            description: 'Declare missing identifier as a module input or internal logic net.',
            before: 'assign y = missing_signal;',
            after: 'input logic [7:0] missing_signal;\nassign y = missing_signal;',
          },
          {
            title: 'Option B: Fix Identifier Spelling Typo',
            description: 'Replace undefined identifier with valid declared signal.',
            before: 'assign y = missing_signal;',
            after: 'assign y = a;',
          },
        ];

      case 'RIVA6002':
        return [
          {
            title: 'Option A: Add Specification Target Signal to RTL',
            description: 'Declare signal specified in requirement [REQ-001] in top module header.',
            before: 'module top(input logic [7:0] a, output logic [7:0] y);',
            after: 'module top(input logic [7:0] a, output logic [7:0] y, output logic [7:0] data_out);',
          },
        ];

      default:
        return [
          {
            title: 'Recommended Code Correction',
            description: suggestionText,
            before: '// Original SystemVerilog assignment\nassign y = expression;',
            after: `// Correction:\n// ${suggestionText}`,
          },
        ];
    }
  };

  const options = getCorrectionOptions();
  const currentOption = options[selectedOption] || options[0];

  const handleCopy = () => {
    navigator.clipboard.writeText(currentOption.after || suggestionText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="p-5 rounded-xl border border-slate-800 bg-[#0B0F10] space-y-4 font-mono text-xs shadow-lg">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2.5">
          <Wrench className="w-4 h-4 text-cyan-400" />
          <span className="font-bold text-sm text-slate-200">Guided Repair Center</span>
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

      {/* AI Grounded Explanation */}
      {aiFinding?.explanation && (
        <div className="bg-cyan-950/20 p-3.5 rounded border border-cyan-900/40 space-y-1">
          <span className="text-[10px] text-cyan-400 uppercase tracking-wider font-semibold flex items-center gap-1">
            <Sparkles className="w-3 h-3" />
            Grounded Reasoning
          </span>
          <p className="text-slate-300 text-xs font-sans leading-relaxed">{aiFinding.explanation}</p>
        </div>
      )}

      {/* Corrected Code Options Tabs (if multiple choices) */}
      {options.length > 1 && (
        <div className="flex items-center gap-2 pt-1">
          <span className="text-[10px] text-slate-500 uppercase tracking-wider font-semibold flex items-center gap-1">
            <Layers className="w-3.5 h-3.5 text-slate-400" />
            Select Fix Approach:
          </span>
          <div className="flex gap-1.5 overflow-x-auto">
            {options.map((opt, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => setSelectedOption(idx)}
                className={`px-2.5 py-1 rounded text-[11px] font-semibold border transition ${
                  selectedOption === idx
                    ? 'bg-cyan-950/60 text-cyan-300 border-cyan-800/80'
                    : 'bg-slate-900 text-slate-400 border-slate-800 hover:text-slate-200'
                }`}
              >
                {opt.title.split(':')[0]}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Code Diff Display (Before vs After) */}
      <div className="bg-[#0d1117] rounded-lg border border-slate-800 overflow-hidden">
        <div className="px-3.5 py-2 bg-slate-950/80 border-b border-slate-800 flex items-center justify-between">
          <span className="text-[11px] font-bold text-emerald-400 flex items-center gap-1.5">
            <Code className="w-3.5 h-3.5 text-emerald-400" />
            {currentOption.title}
          </span>
          <span className="text-[10px] text-slate-500 font-mono">Read-Only Correction Preview</span>
        </div>

        <div className="p-3.5 space-y-3 font-mono text-xs">
          <p className="text-slate-400 font-sans text-xs">{currentOption.description}</p>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {/* Before */}
            <div className="space-y-1">
              <span className="text-[10px] font-bold text-rose-400 uppercase tracking-wider block">Before (Original)</span>
              <pre className="p-2.5 rounded bg-rose-950/20 border border-rose-900/40 text-rose-300 overflow-x-auto leading-relaxed">
                {currentOption.before}
              </pre>
            </div>

            {/* After */}
            <div className="space-y-1">
              <span className="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">After (Corrected)</span>
              <pre className="p-2.5 rounded bg-emerald-950/20 border border-emerald-900/40 text-emerald-300 overflow-x-auto leading-relaxed">
                {currentOption.after}
              </pre>
            </div>
          </div>
        </div>
      </div>

      {/* Action Toolbar */}
      <div className="pt-2 flex items-center justify-between gap-3 border-t border-slate-800">
        <button
          type="button"
          onClick={handleCopy}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 hover:text-cyan-400 transition"
        >
          {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5 text-slate-400" />}
          <span>{copied ? 'Copied Code to Clipboard!' : 'Copy Corrected Code'}</span>
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
