import { Cpu } from 'lucide-react';
import { HierarchyNodeItem } from './HierarchyNode';
import type { HierarchyNode } from '../../types/api';

interface HierarchyExplorerProps {
  hierarchy?: HierarchyNode[];
  topModule?: string;
}

export function HierarchyExplorer({ hierarchy = [], topModule }: HierarchyExplorerProps) {
  if (!hierarchy || hierarchy.length === 0) {
    if (topModule) {
      // Fallback for single top module without parsed children array
      return (
        <div className="p-5 rounded-xl border border-slate-800 bg-[#0B0F10] space-y-3">
          <div className="flex items-center gap-2">
            <Cpu className="w-4 h-4 text-cyan-400" />
            <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Design Hierarchy</h3>
          </div>
          <div className="p-3 rounded bg-slate-950/60 border border-slate-800 font-mono text-xs flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Cpu className="w-4 h-4 text-cyan-400" />
              <span className="font-bold text-slate-200">{topModule}</span>
              <span className="text-[10px] bg-cyan-900/30 text-cyan-400 border border-cyan-800/50 px-1.5 py-0.5 rounded">
                Top Module
              </span>
            </div>
            <span className="text-[11px] text-slate-600">No child instances</span>
          </div>
        </div>
      );
    }

    return (
      <div className="p-5 rounded-xl border border-slate-800 bg-[#0B0F10] space-y-2">
        <div className="flex items-center gap-2">
          <Cpu className="w-4 h-4 text-slate-500" />
          <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Design Hierarchy</h3>
        </div>
        <p className="text-xs text-slate-500 font-mono">No hierarchy information available.</p>
      </div>
    );
  }

  return (
    <div className="p-5 rounded-xl border border-slate-800 bg-[#0B0F10] space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Cpu className="w-4 h-4 text-cyan-400" />
          <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Design Hierarchy</h3>
        </div>
        <span className="text-[10px] font-mono text-slate-500">
          {hierarchy.length} top node{hierarchy.length !== 1 ? 's' : ''}
        </span>
      </div>

      <div className="bg-slate-950/60 p-3 rounded-lg border border-slate-800/80 space-y-1">
        {hierarchy.map((node, idx) => (
          <HierarchyNodeItem
            key={`${node.module_name || node.name || idx}-${idx}`}
            node={node}
            isTop={true}
          />
        ))}
      </div>
    </div>
  );
}
