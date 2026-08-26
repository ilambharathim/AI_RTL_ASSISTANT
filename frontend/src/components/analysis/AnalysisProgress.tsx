import { Activity } from 'lucide-react';

export function AnalysisProgress() {
  return (
    <div className="flex flex-col items-center justify-center h-full text-center gap-8 p-8">
      {/* Spinner ring */}
      <div className="relative w-16 h-16">
        <div className="absolute inset-0 rounded-full border-2 border-slate-800" />
        <div className="absolute inset-0 rounded-full border-2 border-transparent border-t-cyan-400 riva-spinner" />
        <div className="absolute inset-2 rounded-full border border-cyan-900/30 animate-pulse" />
      </div>

      {/* Text */}
      <div className="space-y-2">
        <p className="text-base font-semibold text-slate-100 tracking-wide">Verifying Design</p>
        <p className="text-sm text-slate-500 font-mono max-w-xs leading-relaxed">
          RIVA is analyzing your RTL against the specification…
        </p>
      </div>

      {/* Technical footnote */}
      <div className="flex items-center gap-2 text-[11px] font-mono text-slate-700 bg-slate-900/40 border border-slate-800/60 rounded-lg px-4 py-2">
        <Activity className="w-3 h-3 text-cyan-700 animate-pulse" />
        <span>POST /api/analyze — awaiting response</span>
      </div>
    </div>
  );
}
