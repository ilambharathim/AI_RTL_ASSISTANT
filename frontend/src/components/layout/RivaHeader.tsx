import { Server, Cpu } from 'lucide-react';
import type { AnalysisState } from '../../types/state';

interface RivaHeaderProps {
  analysisState: AnalysisState;
}

export function RivaHeader({ analysisState }: RivaHeaderProps) {
  const isOnline = analysisState.backendOnline && analysisState.status !== 'error';
  const isLoading = analysisState.status === 'loading';

  const statusLabel = () => {
    if (!analysisState.backendOnline) return 'Backend Offline';
    if (isLoading) return 'Verifying…';
    if (analysisState.status === 'success') return 'Ready';
    if (analysisState.status === 'error') return 'Error';
    return 'Ready';
  };

  const statusColor = isLoading
    ? 'text-cyan-400'
    : isOnline
    ? 'text-emerald-400'
    : 'text-rose-400';

  return (
    <header className="flex items-center justify-between px-5 border-b border-slate-800/80 bg-[#0A0D0E] flex-shrink-0" style={{ height: '52px' }}>
      {/* Logo + Title */}
      <div className="flex items-center gap-3">
        <div className="relative">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-600/60 to-cyan-900/80 border border-cyan-700/50 flex items-center justify-center shadow-[0_0_12px_rgba(34,211,238,0.15)]">
            <span className="text-base font-black text-cyan-300 leading-none select-none">R</span>
          </div>
        </div>
        <div className="flex flex-col justify-center">
          <span className="font-bold text-slate-100 text-sm tracking-tight leading-tight">RIVA</span>
          <span className="text-[9px] font-mono text-slate-600 tracking-widest uppercase leading-tight">Verification Workstation</span>
        </div>
        <div className="h-5 w-px bg-slate-800 mx-1" />
        <span className="text-[10px] font-mono text-cyan-600/80 bg-cyan-950/30 border border-cyan-900/40 px-2 py-0.5 rounded">
          v2.0
        </span>
      </div>

      {/* Status cluster */}
      <div className="flex items-center gap-3 text-[11px] font-mono">
        {/* Backend status */}
        <div className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border transition-colors ${
          isLoading
            ? 'bg-cyan-950/30 border-cyan-900/50'
            : isOnline
            ? 'bg-emerald-950/20 border-emerald-900/40'
            : 'bg-rose-950/20 border-rose-900/40'
        }`}>
          <Server className={`w-3.5 h-3.5 ${statusColor} ${isLoading ? 'animate-pulse' : ''}`} />
          <span className={statusColor}>{statusLabel()}</span>
        </div>

        <div className="h-4 w-px bg-slate-800" />

        {/* Edition badge */}
        <div className="flex items-center gap-2 text-slate-500 px-3 py-1.5 rounded-lg bg-slate-900/60 border border-slate-800">
          <Cpu className="w-3.5 h-3.5 text-slate-600" />
          <span className="text-slate-500">Enterprise Edition</span>
        </div>
      </div>
    </header>
  );
}
