import { Activity, AlertTriangle, AlertCircle, Info, Radio, Sparkles, FileCode, CheckCircle2, Clock, Zap } from 'lucide-react';
import type { WaveformResult } from '../../types/api';

interface WaveformPanelProps {
  waveform?: WaveformResult;
}

export function WaveformPanel({ waveform }: WaveformPanelProps) {
  // Case 1: No analysis result / missing waveform object
  if (!waveform) {
    return (
      <div className="p-5 rounded-xl border border-slate-800 bg-[#0B0F10] space-y-2 font-mono text-xs">
        <div className="flex items-center gap-2">
          <Activity className="w-4 h-4 text-slate-500" />
          <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Waveform Analysis</h3>
        </div>
        <p className="text-xs text-slate-500">Waveform analysis unavailable. Run verification first.</p>
      </div>
    );
  }

  // Case 2: Simulator unavailable state
  if (waveform.status === 'unavailable') {
    return (
      <div className="p-5 rounded-xl border border-slate-800 bg-[#0B0F10] space-y-3 font-mono text-xs">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-slate-500" />
            <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Waveform Analysis</h3>
          </div>
          <span className="text-[10px] bg-amber-950/30 text-amber-400 border border-amber-800/50 px-2 py-0.5 rounded font-semibold">
            SIMULATOR UNAVAILABLE
          </span>
        </div>
        <div className="p-3.5 rounded bg-slate-950/60 border border-slate-800/80 text-slate-400 font-sans space-y-1">
          <p className="font-semibold text-slate-300">RTL simulation is unavailable</p>
          <p className="text-xs text-slate-500">
            {waveform.message || 'No supported simulator (such as Icarus Verilog) is installed on the backend server.'}
          </p>
        </div>
      </div>
    );
  }

  // Case 3: No waveform supplied (empty state)
  if (waveform.status === 'empty' || (!waveform.events_count && (!waveform.signals_analyzed || waveform.signals_analyzed.length === 0) && waveform.status !== 'error')) {
    return (
      <div className="p-5 rounded-xl border border-slate-800 bg-[#0B0F10] space-y-3 font-mono text-xs">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-slate-500" />
            <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Waveform Analysis</h3>
          </div>
          <span className="text-[10px] bg-slate-800/60 text-slate-500 border border-slate-700 px-2 py-0.5 rounded">
            NO WAVEFORM
          </span>
        </div>
        <div className="flex items-start gap-2.5 p-3 rounded bg-slate-950/60 border border-slate-800/80 text-slate-400">
          <Info className="w-4 h-4 text-slate-500 flex-shrink-0 mt-0.5" />
          <span>Provide a testbench or upload a VCD trace to analyze simulation waveform activity.</span>
        </div>
      </div>
    );
  }

  // Case 4: Parsing / Processing Error
  if (waveform.status === 'error') {
    const errorObs = waveform.observations?.find(o => o.category === 'PARSING_ERROR') || waveform.observations?.[0];

    return (
      <div className="p-5 rounded-xl border border-rose-900/40 bg-rose-950/10 space-y-3 font-mono text-xs">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-rose-400" />
            <h3 className="text-xs font-semibold text-rose-300 uppercase tracking-wider">Waveform Analysis Error</h3>
          </div>
          <span className="text-[10px] bg-rose-900/30 text-rose-400 border border-rose-800/50 px-2 py-0.5 rounded font-bold">
            PARSING ERROR
          </span>
        </div>
        <p className="text-xs text-rose-200 bg-rose-950/40 p-3 rounded border border-rose-900/50">
          {errorObs ? errorObs.message : 'Malformed or unparseable VCD waveform content encountered.'}
        </p>
      </div>
    );
  }

  // Case 5: Valid Waveform Analysis & Visualization
  const signals = waveform.signals_analyzed ?? [];
  const eventsCount = waveform.events_count ?? 0;
  const observations = waveform.observations ?? [];
  const events = waveform.events ?? [];
  const isGenerated = waveform.source === 'generated';

  const simMeta = waveform.simulation;
  const activity = waveform.signal_activity || {};

  const clockSignals = simMeta?.clock_signals || [];
  const clockFrequencies = simMeta?.clock_frequencies || {};

  // Group events by signal and calculate unique timestamps
  const timestamps = Array.from(new Set(events.map(e => e.timestamp))).sort((a, b) => a - b);

  // Helper to format values for display
  const formatVal = (val: string) => {
    if (!val) return '0';
    if (val === '0' || val === '1') return val;
    const clean = val.replace(/^0+/, '');
    return clean || '0';
  };

  return (
    <div className="p-5 rounded-xl border border-slate-800 bg-[#0B0F10] space-y-5 font-mono text-xs shadow-lg">
      {/* Header & Metrics */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-cyan-950/60 border border-cyan-900/60 flex items-center justify-center text-cyan-400">
            <Activity className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-xs font-semibold text-slate-200 uppercase tracking-wider">Waveform Analysis</h3>
              <span className={`text-[10px] px-2 py-0.5 rounded border font-semibold flex items-center gap-1 ${
                isGenerated
                  ? 'bg-emerald-950/40 text-emerald-400 border-emerald-800/50'
                  : 'bg-cyan-950/40 text-cyan-400 border-cyan-800/50'
              }`}>
                {isGenerated ? (
                  <>
                    <Sparkles className="w-3 h-3 text-emerald-400" />
                    AUTO-GENERATED FROM TESTBENCH
                  </>
                ) : (
                  <>
                    <FileCode className="w-3 h-3 text-cyan-400" />
                    USER-PROVIDED VCD
                  </>
                )}
              </span>
            </div>
            <p className="text-[11px] text-slate-500 mt-0.5 font-sans">
              Simulation trace captured via {isGenerated ? 'RIVA built-in HDL simulator' : 'VCD file stream'}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-5 font-mono text-xs">
          <div>
            <span className="text-[10px] text-slate-500 uppercase tracking-wider block">Duration</span>
            <span className="text-slate-200 font-bold tabular-nums">
              {simMeta?.duration !== undefined ? `${simMeta.duration}ns` : '0ns'}
            </span>
          </div>
          <div className="h-6 w-px bg-slate-800" />
          <div>
            <span className="text-[10px] text-slate-500 uppercase tracking-wider block">Events</span>
            <span className="text-cyan-400 font-bold tabular-nums">{eventsCount}</span>
          </div>
          <div className="h-6 w-px bg-slate-800" />
          <div>
            <span className="text-[10px] text-slate-500 uppercase tracking-wider block">Signals</span>
            <span className="text-slate-200 font-bold tabular-nums">{signals.length}</span>
          </div>
        </div>
      </div>

      {/* Simulation Metadata & Clock Panel */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 p-3.5 rounded-lg bg-slate-950/60 border border-slate-800/80">
        <div className="space-y-1">
          <span className="text-[10px] text-slate-500 uppercase tracking-wider flex items-center gap-1">
            <Clock className="w-3 h-3 text-slate-400" />
            Timescale & Time Window
          </span>
          <p className="text-slate-200 font-bold tabular-nums text-xs">
            {simMeta?.start_time ?? 0}ns → {simMeta?.end_time ?? 0}ns <span className="text-slate-500 text-[10px]">({simMeta?.timescale || '1ns'})</span>
          </p>
        </div>

        <div className="space-y-1 sm:col-span-2">
          <span className="text-[10px] text-slate-500 uppercase tracking-wider flex items-center gap-1">
            <Zap className="w-3 h-3 text-amber-400" />
            Clock Signal & Frequency
          </span>
          {clockSignals.length > 0 ? (
            <div className="flex items-center gap-2">
              {clockSignals.map(clk => (
                <span key={clk} className="text-xs font-bold text-amber-300 bg-amber-950/40 border border-amber-800/50 px-2 py-0.5 rounded">
                  `{clk}`: {clockFrequencies[clk] || 'Active'}
                </span>
              ))}
            </div>
          ) : (
            <p className="text-slate-500 text-xs font-sans">No clock detected (combinational execution)</p>
          )}
        </div>
      </div>

      {/* Truthful Waveform Transition Diagram */}
      {signals.length > 0 && timestamps.length > 0 && (
        <div className="space-y-2">
          <div className="flex items-center justify-between text-[10px] text-slate-500 uppercase tracking-wider">
            <span>Signal Waveform Trace Diagram</span>
            <span>Time Axis ({timestamps.length} sample points)</span>
          </div>

          <div className="bg-[#0d1117] rounded-lg border border-slate-800/80 p-4 font-mono text-xs overflow-x-auto space-y-3">
            {/* Time Header */}
            <div className="flex items-center border-b border-slate-800/80 pb-2 text-[10px] text-slate-500">
              <div className="w-28 flex-shrink-0 font-bold text-slate-400">SIGNAL</div>
              <div className="flex-1 flex justify-between px-2">
                {timestamps.map((t) => (
                  <span key={t} className="text-slate-400 tabular-nums">#{t}ns</span>
                ))}
              </div>
            </div>

            {/* Signal Waveform Rows */}
            {signals.map((sig) => {
              const sigEvents = events.filter(e => e.signal === sig);
              const transitions = activity[sig]?.transitions ?? sigEvents.length;

              return (
                <div key={sig} className="flex items-center py-1 hover:bg-slate-900/40 rounded px-1 transition-colors">
                  {/* Signal Name */}
                  <div className="w-28 flex-shrink-0 flex items-center justify-between gap-1 font-bold text-slate-200 pr-2">
                    <div className="flex items-center gap-1.5 min-w-0">
                      <Radio className="w-3 h-3 text-cyan-400 flex-shrink-0" />
                      <span className="truncate">{sig}</span>
                    </div>
                    <span className="text-[9px] text-slate-500 font-normal tabular-nums">{transitions}t</span>
                  </div>

                  {/* Waveform Step Markers */}
                  <div className="flex-1 flex justify-between items-center px-2">
                    {timestamps.map((t) => {
                      const latest = [...sigEvents].reverse().find(e => e.timestamp <= t) || sigEvents[0];
                      const displayVal = latest ? formatVal(latest.value) : '0';
                      const isHigh = displayVal !== '0';

                      return (
                        <div key={t} className="flex flex-col items-center gap-1 min-w-[32px]">
                          <span className={`px-2 py-0.5 rounded text-[10px] font-bold border tabular-nums ${
                            isHigh
                              ? 'bg-emerald-950/40 text-emerald-300 border-emerald-800/60'
                              : 'bg-slate-900 text-slate-500 border-slate-800'
                          }`}>
                            {displayVal}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Waveform Event Summary */}
      <div className="bg-slate-950/50 p-3 rounded border border-slate-800/80 text-xs flex items-center justify-between">
        <span className="text-slate-400">Captured simulation activity:</span>
        <span className="text-cyan-400 font-semibold flex items-center gap-1">
          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
          {eventsCount} signal transitions recorded
        </span>
      </div>

      {/* Observations */}
      {observations.length > 0 && (
        <div className="space-y-2 pt-1">
          <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block">
            Waveform Observations ({observations.length})
          </span>

          <div className="space-y-2 text-xs">
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
