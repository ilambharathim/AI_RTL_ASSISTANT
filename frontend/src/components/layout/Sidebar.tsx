import { Folder, FileText, Code, FileCode2, ShieldCheck, FileCheck2 } from 'lucide-react';
import type { AnalysisStatus } from '../../types/state';
import type { AnalyzeResponse } from '../../types/api';

interface SidebarProps {
  activeSection: string;
  onNavigate: (section: string) => void;
  analysisStatus: AnalysisStatus;
  analysisResult?: AnalyzeResponse | null;
}

const navItems = [
  { id: 'overview',       label: 'Overview',       icon: Folder,      group: 'input' },
  { id: 'specification',  label: 'Specification',  icon: FileText,    group: 'input' },
  { id: 'rtl',            label: 'RTL',            icon: Code,        group: 'input' },
  { id: 'testbench',      label: 'Testbench',      icon: FileCode2,   group: 'input' },
  { id: 'results',        label: 'Results',        icon: ShieldCheck, group: 'output' },
  { id: 'reports',        label: 'Reports',        icon: FileCheck2,  group: 'output' },
];

export function Sidebar({ activeSection, onNavigate, analysisStatus, analysisResult }: SidebarProps) {
  const getResultsBadge = () => {
    if (analysisStatus !== 'success' || !analysisResult) return null;
    const errors = analysisResult.diagnostics.filter(d => d.severity === 'error').length;
    const warnings = analysisResult.diagnostics.filter(d => d.severity === 'warning').length;

    if (errors > 0) {
      return (
        <span className="ml-auto text-[10px] font-mono px-1.5 py-0.5 rounded bg-rose-900/40 text-rose-400 border border-rose-800/50 font-bold tabular-nums">
          {errors}
        </span>
      );
    }
    if (warnings > 0) {
      return (
        <span className="ml-auto text-[10px] font-mono px-1.5 py-0.5 rounded bg-amber-900/40 text-amber-400 border border-amber-800/50 font-bold tabular-nums">
          {warnings}
        </span>
      );
    }
    return (
      <span className="ml-auto w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_6px_rgba(52,211,153,0.5)]" />
    );
  };

  // Split into input and output groups
  const inputItems  = navItems.filter(i => i.group === 'input');
  const outputItems = navItems.filter(i => i.group === 'output');

  const renderItem = (item: typeof navItems[0]) => {
    const isResultsOrReports = item.id === 'results' || item.id === 'reports';
    const isDisabled = isResultsOrReports && analysisStatus !== 'success';
    const isActive = activeSection === item.id;

    return (
      <button
        key={item.id}
        id={`sidebar-nav-${item.id}`}
        type="button"
        onClick={() => !isDisabled && onNavigate(item.id)}
        disabled={isDisabled}
        aria-current={isActive ? 'page' : undefined}
        title={isDisabled ? 'Run verification first' : item.label}
        className={`w-full flex items-center gap-2.5 px-3 py-2 text-[13px] rounded-lg transition-all duration-150 focus-visible:ring-2 focus-visible:ring-cyan-500/60 ${
          isDisabled
            ? 'text-slate-700 cursor-not-allowed'
            : isActive
            ? 'bg-cyan-950/40 text-cyan-300 border border-cyan-900/50 shadow-[inset_0_0_8px_rgba(34,211,238,0.04)]'
            : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 border border-transparent'
        }`}
      >
        <item.icon className={`w-4 h-4 flex-shrink-0 transition-colors ${
          isDisabled ? 'text-slate-800'
          : isActive  ? 'text-cyan-400'
          : 'text-slate-600 group-hover:text-slate-400'
        }`} />
        <span className="flex-1 text-left font-medium leading-none">{item.label}</span>
        {item.id === 'results' && getResultsBadge()}
      </button>
    );
  };

  return (
    <aside className="w-52 bg-[#0A0D0E] border-r border-slate-800/80 flex flex-col flex-shrink-0">
      {/* Input group */}
      <div className="px-3 pt-3 pb-1">
        <span className="text-[9px] font-mono text-slate-700 uppercase tracking-[0.12em] px-1">Inputs</span>
      </div>
      <nav className="px-2 pb-2 space-y-0.5">
        {inputItems.map(renderItem)}
      </nav>

      {/* Divider */}
      <div className="mx-3 border-t border-slate-800/60 my-1" />

      {/* Output group */}
      <div className="px-3 pt-1 pb-1">
        <span className="text-[9px] font-mono text-slate-700 uppercase tracking-[0.12em] px-1">Analysis</span>
      </div>
      <nav className="px-2 pb-3 space-y-0.5">
        {outputItems.map(renderItem)}
      </nav>

      {/* Bottom spacer */}
      <div className="flex-1" />
      <div className="px-3 py-3 border-t border-slate-800/60">
        <div className="text-[9px] font-mono text-slate-800 text-center tracking-widest">RIVA v2.0</div>
      </div>
    </aside>
  );
}
