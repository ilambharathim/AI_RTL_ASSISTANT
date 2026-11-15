import { useState } from 'react';
import { Cpu, ChevronDown, ChevronRight, Layers, Table } from 'lucide-react';
import type { DesignMetadata } from '../../types/api';

interface DesignOverviewPanelProps {
  metadata?: DesignMetadata;
}

export function DesignOverviewPanel({ metadata }: DesignOverviewPanelProps) {
  const [showSignals, setShowSignals] = useState(true);

  if (!metadata) return null;

  const ops = metadata.operation_counts || {};
  const activeOps = Object.entries(ops).filter(([, count]) => count > 0);

  return (
    <div className="p-5 rounded-xl border border-slate-800 bg-[#0B0F10] space-y-5 font-mono text-xs shadow-lg">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-lg bg-cyan-950/60 border border-cyan-800/60 flex items-center justify-center text-cyan-400">
            <Cpu className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-xs font-semibold text-slate-200 uppercase tracking-wider">Design Overview</h3>
            <p className="text-[10px] text-slate-500 font-sans">Verified SystemVerilog AST & Semantic Model</p>
          </div>
        </div>

        <span className="text-[11px] font-bold text-cyan-400 bg-cyan-950/40 border border-cyan-900/60 px-2.5 py-1 rounded">
          Top: `{metadata.top_module}`
        </span>
      </div>

      {/* Metrics Cards Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div className="p-3 rounded-lg bg-slate-950/60 border border-slate-800/80">
          <span className="text-[10px] text-slate-500 uppercase tracking-wider block">Modules / Instances</span>
          <span className="text-slate-200 font-bold text-sm tabular-nums mt-0.5 block">
            {metadata.module_count} <span className="text-slate-500 text-xs font-normal">/ {metadata.instance_count} inst</span>
          </span>
        </div>

        <div className="p-3 rounded-lg bg-slate-950/60 border border-slate-800/80">
          <span className="text-[10px] text-slate-500 uppercase tracking-wider block">Ports (In / Out)</span>
          <span className="text-slate-200 font-bold text-sm tabular-nums mt-0.5 block">
            {metadata.port_count} <span className="text-slate-500 text-xs font-normal">({metadata.input_count}in / {metadata.output_count}out)</span>
          </span>
        </div>

        <div className="p-3 rounded-lg bg-slate-950/60 border border-slate-800/80">
          <span className="text-[10px] text-slate-500 uppercase tracking-wider block">Signals & Nets</span>
          <span className="text-cyan-400 font-bold text-sm tabular-nums mt-0.5 block">
            {metadata.signal_count} <span className="text-slate-500 text-xs font-normal">total</span>
          </span>
        </div>

        <div className="p-3 rounded-lg bg-slate-950/60 border border-slate-800/80">
          <span className="text-[10px] text-slate-500 uppercase tracking-wider block">Assignments</span>
          <span className="text-slate-200 font-bold text-sm tabular-nums mt-0.5 block">
            {metadata.assignment_count} <span className="text-slate-500 text-xs font-normal">({metadata.always_block_count} always)</span>
          </span>
        </div>
      </div>

      {/* RTL Operations Summary */}
      <div className="space-y-2">
        <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider flex items-center gap-1.5">
          <Layers className="w-3.5 h-3.5 text-slate-400" />
          RTL Operations ({activeOps.length > 0 ? activeOps.length : '0'} active types)
        </span>

        {activeOps.length > 0 ? (
          <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-6 gap-2">
            {activeOps.map(([opName, count]) => (
              <div key={opName} className="p-2 rounded bg-slate-950/60 border border-slate-800/80 flex items-center justify-between">
                <span className="text-slate-400 font-bold">{opName}</span>
                <span className="text-cyan-400 font-bold tabular-nums bg-cyan-950/40 px-1.5 py-0.5 rounded border border-cyan-900/40 text-[10px]">
                  {count}
                </span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-slate-500 text-xs font-sans">No complex arithmetic/logic operations detected in continuous assignments.</p>
        )}
      </div>

      {/* Collapsible Signal Intelligence Table */}
      {metadata.signals && metadata.signals.length > 0 && (
        <div className="space-y-2 pt-1 border-t border-slate-800/80">
          <button
            type="button"
            onClick={() => setShowSignals(!showSignals)}
            className="flex items-center gap-1.5 text-[10px] font-semibold text-slate-400 hover:text-slate-200 uppercase tracking-wider transition"
          >
            {showSignals ? <ChevronDown className="w-3.5 h-3.5" /> : <ChevronRight className="w-3.5 h-3.5" />}
            <Table className="w-3.5 h-3.5 text-cyan-400" />
            Signal Intelligence ({metadata.signals.length} declared nets)
          </button>

          {showSignals && (
            <div className="bg-[#0d1117] rounded-lg border border-slate-800 overflow-x-auto">
              <table className="w-full text-left font-mono text-xs">
                <thead>
                  <tr className="border-b border-slate-800 bg-slate-950/80 text-[10px] text-slate-500 uppercase tracking-wider">
                    <th className="py-2 px-3 font-semibold">Signal</th>
                    <th className="py-2 px-3 font-semibold">Direction</th>
                    <th className="py-2 px-3 font-semibold">Data Type</th>
                    <th className="py-2 px-3 font-semibold">Width</th>
                    <th className="py-2 px-3 font-semibold">Signedness</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 text-slate-300">
                  {metadata.signals.map((sig, idx) => {
                    const isInput = sig.direction === 'input';
                    const isOutput = sig.direction === 'output';

                    return (
                      <tr key={`${sig.name}-${idx}`} className="hover:bg-slate-900/40 transition">
                        <td className="py-2 px-3 font-bold text-slate-100">{sig.name}</td>
                        <td className="py-2 px-3">
                          <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded border uppercase ${
                            isInput
                              ? 'bg-cyan-950/60 text-cyan-400 border-cyan-800/50'
                              : isOutput
                              ? 'bg-emerald-950/60 text-emerald-400 border-emerald-800/50'
                              : 'bg-slate-800 text-slate-400 border-slate-700'
                          }`}>
                            {sig.direction}
                          </span>
                        </td>
                        <td className="py-2 px-3 text-slate-400">{sig.data_type}</td>
                        <td className="py-2 px-3 text-slate-200 font-bold tabular-nums">
                          {sig.width} {sig.width === 1 ? 'bit' : 'bits'}
                        </td>
                        <td className="py-2 px-3 text-slate-500">
                          {sig.signed ? 'signed' : 'unsigned'}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
