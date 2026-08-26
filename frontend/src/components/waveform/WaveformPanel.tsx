import { Activity, AlertTriangle, AlertCircle, Info, Radio } from 'lucide-react';
import type { WaveformResult } from '../../types/api';

interface WaveformPanelProps {
  waveform?: WaveformResult;
}

export function WaveformPanel({ waveform }: WaveformPanelProps) {
  // Case 1: No analysis result / missing waveform object
  if (!waveform) {
    return (
      <div className="p-5 rounded-xl border border-slate-800 bg-[#0B0F10] space-y-2">
        <div className="flex items-center gap-2">
          <Activity className="w-4 h-4 text-slate-500" />
          <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Waveform Analysis</h3>
        </div>
        <p className="text-xs text-slate-500 font-mono">Waveform analysis unavailable. Run verification first.</p>
      </div>
    );
  }

  // Case 2: No waveform supplied (empty state)
  if (waveform.status === 'empty' || (!waveform.events_count && (!waveform.signals_analyzed || waveform.signals_analyzed.length === 0) && waveform.status !== 'error')) {
    return (
      <div className="p-5 rounded-xl border border-slate-800 bg-[#0B0F10] space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-slate-500" />
            <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Waveform Analysis</h3>
          </div>
          <span className="text-[10px] font-mono bg-slate-800/60 text-slate-500 border border-slate-700 px-2 py-0.5 rounded">
            NO WAVEFORM
          </span>
        </div>
        <div className="flex items-start gap-2.5 p-3 rounded bg-slate-950/60 border border-slate-800/80 text-xs text-slate-400 font-mono">
          <Info className="w-4 h-4 text-slate-500 flex-shrink-0 mt-0.5" />
          <span>No waveform provided. Submit a VCD waveform with the testbench to inspect signal activity.</span>
        </div>
      </div>
    );
  }

  // Case 3: Parsing / Processing Error
  if (waveform.status === 'error') {
    const errorObs = waveform.observations?.find(o => o.category === 'PARSING_ERROR') || waveform.observations?.[0];

    return (
      <div className="p-5 rounded-xl border border-rose-900/40 bg-rose-950/10 space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-rose-400" />
            <h3 className="text-xs font-semibold text-rose-300 uppercase tracking-wider">Waveform Analysis Error</h3>
          </div>
          <span className="text-[10px] font-mono bg-rose-900/30 text-rose-400 border border-rose-800/50 px-2 py-0.5 rounded font-bold">
            PARSING ERROR
          </span>
        </div>
        <p className="text-xs text-rose-200 font-mono bg-rose-950/40 p-3 rounded border border-rose-900/50">
          {errorObs ? errorObs.message : 'Malformed or unparseable VCD waveform content encountered.'}
        </p>
      </div>
    );
  }

  // Case 4: Valid Waveform Analysis
  const signals = waveform.signals_analyzed ?? [];
  const eventsCount = waveform.events_count ?? 0;
  const observations = waveform.observations ?? [];

  return (
    <div className="p-5 rounded-xl border border-slate-800 bg-[#0B0F10] space-y-5">
      {/* Header & Metrics */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <Activity className="w-4 h-4 text-cyan-400" />
          <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Waveform Analysis</h3>
        </div>

        <div className="flex items-center gap-6 font-mono text-xs">
          <div>
            <span className="text-[10px] text-slate-500 uppercase tracking-wider block">Status</span>
            <span className="text-emerald-400 font-bold">Available</span>
          </div>
          <div className="h-6 w-px bg-slate-800" />
          <div>
            <span className="text-[10px] text-slate-500 uppercase tracking-wider block">Events</span>
            <span className="text-cyan-400 font-bold">{eventsCount}</span>
          </div>
          <div className="h-6 w-px bg-slate-800" />
          <div>
            <span className="text-[10px] text-slate-500 uppercase tracking-wider block">Signals</span>
            <span className="text-slate-200 font-bold">{signals.length}</span>
          </div>
        </div>
      </div>

      {/* Signals Analyzed List */}
      <div className="space-y-2">
        <span className="text-[10px] font-mono font-semibold text-slate-500 uppercase tracking-wider block">
          Signals Analyzed ({signals.length})
        </span>

        {signals.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2 font-mono text-xs">
            {signals.map((sig, idx) => (
              <div
                key={`${sig}-${idx}`}
                className="flex items-center gap-2.5 p-2.5 rounded bg-slate-950/60 border border-slate-800/80 hover:border-slate-700 transition"
              >
                <Radio className="w-3.5 h-3.5 text-cyan-400 flex-shrink-0" />
                <span className="font-semibold text-slate-200 truncate">{sig}</span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-slate-500 font-mono">No signal definitions extracted from VCD trace header.</p>
        )}
      </div>

      {/* Waveform Event Summary */}
      <div className="bg-slate-950/50 p-3.5 rounded border border-slate-800/80 font-mono text-xs flex items-center justify-between">
        <span className="text-slate-400">Activity trace summary:</span>
        <span className="text-cyan-400 font-semibold">{eventsCount} total signal transition event{eventsCount !== 1 ? 's' : ''} logged</span>
      </div>

      {/* Observations & Raw Evidence */}
      {observations.length > 0 && (
        <div className="space-y-2 pt-1">
          <span className="text-[10px] font-mono font-semibold text-slate-500 uppercase tracking-wider block">
            Waveform Observations ({observations.length})
          </span>

          <div className="space-y-2 font-mono text-xs">
            {observations.map((obs, idx) => {
              const isGlitch = obs.category === 'GLITCH';
              const isToggle = obs.category === 'TOGGLE_ACTIVITY';

              return (
                <div
                  key={idx}
                  className={`flex items-start gap-3 p-3 rounded border ${
                    isGlitch
                      ? 'bg-rose-950/20 border-rose-900/40 text-rose-300'
                      : isToggle
                      ? 'bg-amber-950/20 border-amber-900/40 text-amber-300'
                      : 'bg-slate-950/60 border-slate-800 text-slate-300'
                  }`}
                >
                  {isGlitch ? (
                    <AlertCircle className="w-4 h-4 text-rose-400 flex-shrink-0 mt-0.5" />
                  ) : isToggle ? (
                    <AlertTriangle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
                  ) : (
                    <Info className="w-4 h-4 text-cyan-400 flex-shrink-0 mt-0.5" />
                  )}

                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-2 mb-0.5">
                      <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded border uppercase ${
                        isGlitch
                          ? 'bg-rose-900/40 text-rose-400 border-rose-800/50'
                          : isToggle
                          ? 'bg-amber-900/40 text-amber-400 border-amber-800/50'
                          : 'bg-cyan-900/40 text-cyan-400 border-cyan-800/50'
                      }`}>
                        {obs.category}
                      </span>
                      {obs.signal_name && (
                        <span className="text-slate-400 font-semibold">{obs.signal_name}</span>
                      )}
                      {obs.timestamp !== undefined && obs.timestamp > 0 && (
                        <span className="text-[10px] text-slate-500 ml-auto">t={obs.timestamp}ns</span>
                      )}
                    </div>
                    <p className="font-sans text-xs text-slate-300">{obs.message}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
