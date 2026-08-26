import { AlertCircle, RefreshCw } from 'lucide-react';

interface AnalysisErrorProps {
  message: string;
  onRetry: () => void;
}

export function AnalysisError({ message, onRetry }: AnalysisErrorProps) {
  return (
    <div className="flex flex-col items-center justify-center h-full text-center gap-6 max-w-md mx-auto p-8">
      <div className="w-14 h-14 rounded-full bg-rose-950/20 border border-rose-800/40 flex items-center justify-center shadow-[0_0_20px_rgba(244,63,94,0.06)]">
        <AlertCircle className="w-7 h-7 text-rose-400" />
      </div>

      <div className="space-y-2">
        <p className="text-rose-400 font-semibold text-base tracking-tight">Verification Failed</p>
        <p className="text-slate-400 text-sm leading-relaxed font-sans max-w-sm">
          {message}
        </p>
      </div>

      <button
        type="button"
        onClick={onRetry}
        className="flex items-center gap-2 px-5 py-2.5 rounded-lg bg-slate-800/60 border border-slate-700 text-slate-300 hover:border-cyan-700 hover:text-cyan-400 hover:bg-slate-800/80 transition-all duration-150 text-sm font-medium focus-visible:ring-2 focus-visible:ring-cyan-500/60"
      >
        <RefreshCw className="w-4 h-4" />
        Retry Verification
      </button>
    </div>
  );
}
