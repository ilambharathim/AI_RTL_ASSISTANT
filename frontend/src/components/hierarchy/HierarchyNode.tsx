import { useState } from 'react';
import { ChevronRight, ChevronDown, Cpu, Box } from 'lucide-react';
import type { HierarchyNode as HierarchyNodeType } from '../../types/api';

interface HierarchyNodeProps {
  node: HierarchyNodeType;
  level?: number;
  isTop?: boolean;
}

export function HierarchyNodeItem({ node, level = 0, isTop = false }: HierarchyNodeProps) {
  const [isExpanded, setIsExpanded] = useState(isTop);

  const moduleName = node.module_name || node.name || 'Unnamed Module';
  const instanceName = node.instance_name || (isTop ? 'top_level' : null);
  const children = node.children || [];
  const hasChildren = children.length > 0;
  const parameters = node.parameters;
  const paramKeys = parameters ? Object.keys(parameters) : [];

  return (
    <div className="font-mono text-xs select-none">
      <div
        onClick={() => hasChildren && setIsExpanded(!isExpanded)}
        onKeyDown={(e) => {
          if (hasChildren && (e.key === 'Enter' || e.key === ' ')) {
            e.preventDefault();
            setIsExpanded(!isExpanded);
          }
        }}
        tabIndex={hasChildren ? 0 : -1}
        role={hasChildren ? 'button' : undefined}
        aria-expanded={hasChildren ? isExpanded : undefined}
        className={`flex items-center gap-2 py-1.5 px-2 rounded-md transition ${
          hasChildren ? 'cursor-pointer hover:bg-slate-900/60' : ''
        }`}
        style={{ paddingLeft: `${level * 16 + 8}px` }}
      >
        {/* Toggle Icon */}
        {hasChildren ? (
          <span className="text-slate-500 hover:text-slate-300">
            {isExpanded ? <ChevronDown className="w-3.5 h-3.5" /> : <ChevronRight className="w-3.5 h-3.5" />}
          </span>
        ) : (
          <span className="w-3.5 h-3.5 text-slate-700 flex justify-center items-center font-mono">
            └
          </span>
        )}

        {/* Module / Instance Icon */}
        {isTop ? (
          <Cpu className="w-4 h-4 text-cyan-400 flex-shrink-0" />
        ) : (
          <Box className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0" />
        )}

        {/* Instance & Module Name */}
        <div className="flex items-center gap-2 min-w-0">
          {instanceName && !isTop && (
            <span className="font-semibold text-cyan-300">{instanceName}</span>
          )}
          {instanceName && !isTop && <span className="text-slate-600">:</span>}
          <span className="text-slate-200 font-bold">{moduleName}</span>
          {isTop && (
            <span className="text-[10px] bg-cyan-900/30 text-cyan-400 border border-cyan-800/50 px-1.5 py-0.5 rounded font-mono">
              Top Module
            </span>
          )}
        </div>

        {/* Parameter Badges */}
        {paramKeys.length > 0 && (
          <div className="ml-auto flex items-center gap-1">
            {paramKeys.map((key) => (
              <span
                key={key}
                className="text-[9px] font-mono bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded border border-slate-700"
              >
                {key}={String(parameters?.[key])}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Child Nodes */}
      {hasChildren && isExpanded && (
        <div className="border-l border-slate-800/80 ml-4 pl-1">
          {children.map((child, idx) => (
            <HierarchyNodeItem
              key={`${child.instance_name || child.module_name || idx}-${idx}`}
              node={child}
              level={level + 1}
            />
          ))}
        </div>
      )}
    </div>
  );
}
