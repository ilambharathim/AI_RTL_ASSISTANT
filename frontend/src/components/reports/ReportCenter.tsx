import { useState } from 'react';
import { FileText, Code2, Copy, Download, Printer, Check, ShieldCheck, AlertCircle, CheckCircle2 } from 'lucide-react';
import type { AnalysisState } from '../../types/state';

interface ReportCenterProps {
  analysisState: AnalysisState;
  projectName?: string;
}

export function ReportCenter({ analysisState, projectName = "RIVA Verification Project" }: ReportCenterProps) {
  const [activeTab, setActiveTab] = useState<'markdown' | 'json'>('markdown');
  const [copiedMd, setCopiedMd] = useState(false);
  const [copiedJson, setCopiedJson] = useState(false);

  const { status, result, error } = analysisState;

  // 1. No Analysis State
  if (status === 'idle' || !result) {
    return (
      <div className="flex flex-col items-center justify-center h-full p-8 text-center space-y-3 font-mono text-xs">
        <div className="w-12 h-12 rounded-full bg-slate-900 border border-slate-800 flex items-center justify-center text-slate-600">
          <FileText className="w-6 h-6" />
        </div>
        <h3 className="text-sm font-bold text-slate-400">NO REPORT AVAILABLE</h3>
        <p className="text-slate-500 font-sans max-w-sm">
          Run verification to generate consolidated engineering Markdown and JSON reports.
        </p>
      </div>
    );
  }

  // 2. Analysis Error State
  if (status === 'error') {
    return (
      <div className="flex flex-col items-center justify-center h-full p-8 text-center space-y-3 font-mono text-xs">
        <div className="w-12 h-12 rounded-full bg-rose-950/40 border border-rose-900/60 flex items-center justify-center text-rose-400">
          <AlertCircle className="w-6 h-6" />
        </div>
        <h3 className="text-sm font-bold text-rose-400">REPORT UNAVAILABLE</h3>
        <p className="text-slate-400 font-sans max-w-md">
          {error || 'Verification pipeline encountered an error.'}
        </p>
      </div>
    );
  }

  const reports = result.reports;
  const markdownText = reports?.markdown ?? '';
  const jsonText = reports?.json ?? '';

  const errorsCount = result.diagnostics.filter(d => d.severity === 'error').length;
  const warningsCount = result.diagnostics.filter(d => d.severity === 'warning').length;
  const reqPassed = result.traceability.filter(t => t.status === 'PASSED').length;
  const reqTotal = result.traceability.length;
  const waveformAvailable = result.waveform?.status === 'success';
  const confidenceScore = result.explanation?.confidence_score ?? 95;

  const isClean = errorsCount === 0;

  // Copy Actions
  const handleCopyMarkdown = () => {
    navigator.clipboard.writeText(markdownText);
    setCopiedMd(true);
    setTimeout(() => setCopiedMd(false), 2000);
  };

  const handleCopyJson = () => {
    navigator.clipboard.writeText(jsonText);
    setCopiedJson(true);
    setTimeout(() => setCopiedJson(false), 2000);
  };

  // Download Actions
  const handleDownloadMarkdown = () => {
    const blob = new Blob([markdownText], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${projectName.toLowerCase().replace(/[^a-z0-9]/g, '-')}-report.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleDownloadJson = () => {
    const blob = new Blob([jsonText], { type: 'application/json;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${projectName.toLowerCase().replace(/[^a-z0-9]/g, '-')}-report.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // Print Action
  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="max-w-4xl mx-auto w-full py-4 space-y-6">
      {/* Report Header Card */}
      <div className="p-6 rounded-xl border border-slate-800 bg-[#0B0F10] space-y-4 shadow-lg">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded bg-cyan-950/50 border border-cyan-900/60 flex items-center justify-center text-cyan-400">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-100">{projectName}</h2>
              <p className="text-xs font-mono text-slate-500">
                Top Module: <span className="text-cyan-400">{result.top_module || '—'}</span>
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 font-mono text-xs">
            <span className={`px-2.5 py-1 rounded border font-bold uppercase ${
              isClean
                ? 'bg-emerald-950/30 text-emerald-400 border-emerald-800/50'
                : 'bg-rose-950/30 text-rose-400 border-rose-800/50'
            }`}>
              {isClean ? 'VERIFICATION PASSED' : 'VERIFICATION FAILED'}
            </span>
          </div>
        </div>

        {/* Verification Summary Metrics Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 font-mono text-xs pt-1">
          <div className="bg-slate-950/60 p-3 rounded border border-slate-800/80">
            <span className="text-[10px] text-slate-500 uppercase tracking-wider block">Diagnostics</span>
            <span className={`text-sm font-bold ${errorsCount > 0 ? 'text-rose-400' : 'text-emerald-400'}`}>
              {errorsCount} errors / {warningsCount} warnings
            </span>
          </div>

          <div className="bg-slate-950/60 p-3 rounded border border-slate-800/80">
            <span className="text-[10px] text-slate-500 uppercase tracking-wider block">Requirements</span>
            <span className="text-sm font-bold text-cyan-400">
              {reqPassed} / {reqTotal} passed
            </span>
          </div>

          <div className="bg-slate-950/60 p-3 rounded border border-slate-800/80">
            <span className="text-[10px] text-slate-500 uppercase tracking-wider block">Waveform Trace</span>
            <span className={`text-sm font-bold ${waveformAvailable ? 'text-emerald-400' : 'text-slate-500'}`}>
              {waveformAvailable ? 'Available' : 'Not provided'}
            </span>
          </div>

          <div className="bg-slate-950/60 p-3 rounded border border-slate-800/80">
            <span className="text-[10px] text-slate-500 uppercase tracking-wider block">Grounded Confidence</span>
            <span className="text-sm font-bold text-cyan-400 flex items-center gap-1">
              <CheckCircle2 className="w-3.5 h-3.5" />
              {confidenceScore}%
            </span>
          </div>
        </div>
      </div>

      {/* Toolbar & Tabs */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 bg-[#0B0F10] p-3 rounded-xl border border-slate-800 font-mono text-xs">
        {/* Tabs */}
        <div className="flex items-center gap-1 bg-slate-950 p-1 rounded-lg border border-slate-800">
          <button
            type="button"
            onClick={() => setActiveTab('markdown')}
            className={`px-3 py-1.5 rounded transition flex items-center gap-2 font-semibold ${
              activeTab === 'markdown'
                ? 'bg-cyan-900/40 text-cyan-400 border border-cyan-800/60'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <FileText className="w-3.5 h-3.5" />
            Markdown Report
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('json')}
            className={`px-3 py-1.5 rounded transition flex items-center gap-2 font-semibold ${
              activeTab === 'json'
                ? 'bg-cyan-900/40 text-cyan-400 border border-cyan-800/60'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Code2 className="w-3.5 h-3.5" />
            JSON Report
          </button>
        </div>

        {/* Export Toolbar */}
        <div className="flex items-center gap-2 flex-wrap">
          {activeTab === 'markdown' ? (
            <>
              <button
                type="button"
                onClick={handleCopyMarkdown}
                className="px-3 py-1.5 rounded bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 transition flex items-center gap-1.5"
              >
                {copiedMd ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5 text-slate-400" />}
                <span>{copiedMd ? 'Copied' : 'Copy Markdown'}</span>
              </button>
              <button
                type="button"
                onClick={handleDownloadMarkdown}
                className="px-3 py-1.5 rounded bg-slate-900 hover:bg-slate-800 border border-slate-700 text-cyan-400 transition flex items-center gap-1.5 font-semibold"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Download Markdown</span>
              </button>
            </>
          ) : (
            <>
              <button
                type="button"
                onClick={handleCopyJson}
                className="px-3 py-1.5 rounded bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 transition flex items-center gap-1.5"
              >
                {copiedJson ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5 text-slate-400" />}
                <span>{copiedJson ? 'Copied' : 'Copy JSON'}</span>
              </button>
              <button
                type="button"
                onClick={handleDownloadJson}
                className="px-3 py-1.5 rounded bg-slate-900 hover:bg-slate-800 border border-slate-700 text-cyan-400 transition flex items-center gap-1.5 font-semibold"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Download JSON</span>
              </button>
            </>
          )}

          <div className="h-4 w-px bg-slate-800 hidden sm:block" />

          <button
            type="button"
            onClick={handlePrint}
            className="px-3 py-1.5 rounded bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 transition flex items-center gap-1.5"
          >
            <Printer className="w-3.5 h-3.5 text-slate-400" />
            <span>Print Report</span>
          </button>
        </div>
      </div>

      {/* Main Report View Container */}
      <div className="p-6 rounded-xl border border-slate-800 bg-[#0B0F10] shadow-xl overflow-x-auto print:bg-white print:text-black">
        {activeTab === 'markdown' ? (
          <pre className="font-mono text-xs text-slate-200 whitespace-pre-wrap leading-relaxed select-text font-sans">
            {markdownText || 'No Markdown report generated by backend.'}
          </pre>
        ) : (
          <pre className="font-mono text-xs text-cyan-300 bg-slate-950/80 p-4 rounded border border-slate-800/80 whitespace-pre-wrap select-text">
            {jsonText || 'No JSON report generated by backend.'}
          </pre>
        )}
      </div>
    </div>
  );
}
