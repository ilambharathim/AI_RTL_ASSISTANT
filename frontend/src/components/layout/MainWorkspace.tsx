
import { Play } from 'lucide-react';

export function MainWorkspace() {
  // Only displaying the welcome/project state for Phase 1 as requested.
  // When activeSection is overview or anything, show the primary workspace.

  return (
    <main className="flex-1 p-8 overflow-y-auto relative z-10">
      <div className="max-w-4xl mx-auto mt-12 flex flex-col items-center justify-center text-center space-y-6">

        <div className="w-20 h-20 bg-[#0F1516] border border-cyan-900/50 rounded-2xl flex items-center justify-center shadow-[0_0_30px_rgba(34,211,238,0.1)] mb-4">
           <span className="text-3xl font-bold text-cyan-400 font-serif">R</span>
        </div>

        <h1 className="text-4xl font-bold text-slate-100 tracking-tight">RIVA</h1>

        <h2 className="text-xl text-slate-300 font-medium">
          RTL Verification & Intelligent Verification Assistant
        </h2>

        <p className="text-slate-400 max-w-lg leading-relaxed text-sm">
          "Verify your design against specification, testbench and implementation evidence."
        </p>

        <div className="pt-8 flex gap-4">
          <button
            disabled
            className="px-6 py-3 rounded bg-cyan-900/30 text-cyan-400 font-medium border border-cyan-800/50 opacity-60 cursor-not-allowed flex items-center gap-2 transition"
          >
            Create / Open Project
          </button>
          <button
            disabled
            className="px-6 py-3 rounded bg-emerald-600/30 text-emerald-400 font-medium border border-emerald-500/50 opacity-60 cursor-not-allowed flex items-center gap-2 transition shadow-[0_0_15px_rgba(16,185,129,0.1)]"
          >
            <Play className="w-4 h-4" />
            Start Verification
          </button>
        </div>

        <p className="text-xs font-mono text-slate-600 mt-8 pt-12">
          Workspace currently in empty state. Load a project to begin analysis.
        </p>

      </div>
    </main>
  );
}
