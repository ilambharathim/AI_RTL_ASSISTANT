import { useState, useRef } from 'react';
import { Trash2, Code, FileText, FileCode2, Activity, UploadCloud, Dot } from 'lucide-react';
import type { ProjectState } from '../../types/state';

interface EditorToolbarProps {
  activeSection: string;
  projectState: ProjectState;
  setProjectState: React.Dispatch<React.SetStateAction<ProjectState>>;
}

const SECTION_META: Record<string, { label: string; subtitle: string; fileTypes: string; dirty: keyof ProjectState; code: keyof ProjectState }> = {
  specification: {
    label: 'Specification',
    subtitle: 'Natural language requirements',
    fileTypes: '.txt,.spec,.md',
    dirty: 'isDirtySpec',
    code: 'specCode',
  },
  rtl: {
    label: 'SystemVerilog RTL',
    subtitle: 'Hardware description — parsed by the backend',
    fileTypes: '.sv,.v',
    dirty: 'isDirtyRtl',
    code: 'rtlCode',
  },
  testbench: {
    label: 'Testbench',
    subtitle: 'Simulation stimulus module (optional)',
    fileTypes: '.sv,.v',
    dirty: 'isDirtyTb',
    code: 'testbenchCode',
  },
  waveform: {
    label: 'Waveform (VCD)',
    subtitle: 'Value change dump trace (optional)',
    fileTypes: '.vcd',
    dirty: 'isDirtyVcd',
    code: 'vcdContent',
  },
};

const SECTION_ICONS: Record<string, React.FC<{ className?: string }>> = {
  specification: FileText,
  rtl: Code,
  testbench: FileCode2,
  waveform: Activity,
};

export function EditorToolbar({ activeSection, projectState, setProjectState }: EditorToolbarProps) {
  const [confirmClear, setConfirmClear] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const meta = SECTION_META[activeSection];
  const Icon = SECTION_ICONS[activeSection] ?? Code;

  if (!meta) return null;

  const currentCode = projectState[meta.code] as string;
  const isDirty = projectState[meta.dirty] as boolean;
  const lineCount = currentCode ? currentCode.split('\n').length : 0;
  const charCount = currentCode.length;
  const isEmpty = !currentCode.trim();
  const isOptional = activeSection === 'testbench' || activeSection === 'waveform';

  const handleClear = () => {
    if (!confirmClear) {
      setConfirmClear(true);
      return;
    }
    setProjectState(prev => ({ ...prev, [meta.code]: '', [meta.dirty]: false }));
    setConfirmClear(false);
  };

  const handleFileLoad = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => {
      const text = event.target?.result as string;
      setProjectState(prev => ({ ...prev, [meta.code]: text, [meta.dirty]: true }));
    };
    reader.readAsText(file);
    e.target.value = '';
  };

  return (
    <div className="flex items-center justify-between px-5 py-3 border-b border-slate-800/70 bg-[#0F1516]/80 flex-shrink-0">
      {/* Left: file info */}
      <div className="flex items-center gap-3 min-w-0">
        <Icon className="w-4 h-4 text-cyan-500 flex-shrink-0" />
        <div className="min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-sm font-semibold text-slate-200 leading-none">{meta.label}</span>

            {/* Status badge */}
            {!isEmpty ? (
              <span className="text-[10px] font-mono bg-emerald-950/40 text-emerald-400 border border-emerald-800/50 px-1.5 py-0.5 rounded leading-none">
                Ready
              </span>
            ) : (
              <span className="text-[10px] font-mono bg-slate-800/50 text-slate-500 border border-slate-700/60 px-1.5 py-0.5 rounded leading-none">
                {isOptional ? 'Optional' : 'Empty'}
              </span>
            )}

            {/* Unsaved indicator */}
            {isDirty && (
              <span className="text-[10px] font-mono text-amber-400 flex items-center gap-1 leading-none">
                <Dot className="w-4 h-4 -mx-1 text-amber-400" />
                Unsaved
              </span>
            )}
          </div>
          <p className="text-[11px] text-slate-600 mt-1 leading-none truncate">{meta.subtitle}</p>
        </div>
      </div>

      {/* Right: stats + actions */}
      <div className="flex items-center gap-2 text-[11px] font-mono text-slate-500 flex-shrink-0 ml-4">
        {!isEmpty && (
          <span className="hidden sm:block text-slate-700 tabular-nums">
            {lineCount}L · {charCount}C
          </span>
        )}

        {/* Load file */}
        <button
          type="button"
          onClick={() => fileInputRef.current?.click()}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800/50 text-slate-300 border border-slate-700/60 hover:border-cyan-700/60 hover:text-cyan-400 hover:bg-slate-800/80 transition-all duration-150 focus-visible:ring-2 focus-visible:ring-cyan-500/50"
        >
          <UploadCloud className="w-3.5 h-3.5" />
          <span>Load file</span>
        </button>
        <input
          ref={fileInputRef}
          type="file"
          accept={meta.fileTypes}
          className="hidden"
          onChange={handleFileLoad}
          aria-label={`Load ${meta.label} file`}
        />

        {/* Clear — only shown when content exists */}
        {!isEmpty && (
          <button
            type="button"
            onClick={handleClear}
            onBlur={() => setConfirmClear(false)}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg border transition-all duration-150 focus-visible:ring-2 ${
              confirmClear
                ? 'bg-rose-950/40 text-rose-400 border-rose-700/60 hover:bg-rose-900/50 focus-visible:ring-rose-500/50'
                : 'bg-slate-800/50 text-slate-400 border-slate-700/60 hover:border-rose-700/60 hover:text-rose-400 focus-visible:ring-rose-500/40'
            }`}
          >
            <Trash2 className="w-3.5 h-3.5" />
            <span>{confirmClear ? 'Confirm clear?' : 'Clear'}</span>
          </button>
        )}
      </div>
    </div>
  );
}
