import { RivaHeader } from './RivaHeader';
import { Sidebar } from './Sidebar';
import { ContextPanel } from './ContextPanel';
import { StatusBar } from './StatusBar';
import { useRivaState } from '../../hooks/useRivaState';
import { VerificationWorkspace } from '../editor/VerificationWorkspace';
import { AnalysisProgress } from '../analysis/AnalysisProgress';
import { AnalysisError } from '../analysis/AnalysisError';
import { AnalysisResultSummary } from '../analysis/AnalysisResultSummary';
import { ReportCenter } from '../reports/ReportCenter';

export function RivaShell() {
  const {
    analysisState,
    projectState,
    setProjectState,
    inputStatus,
    uiState,
    setActiveSection,
    runAnalysis,
  } = useRivaState();

  const activeSection = uiState.activeSection;

  const renderMain = () => {
    // During loading, show the spinner
    if (analysisState.status === 'loading') {
      return (
        <main className="flex-1 p-6 overflow-hidden relative z-10 flex flex-col">
          <AnalysisProgress />
        </main>
      );
    }

    // Reports section
    if (activeSection === 'reports') {
      return (
        <main className="flex-1 p-6 overflow-y-auto relative z-10 flex flex-col">
          <ReportCenter
            analysisState={analysisState}
            projectName={projectState.projectName}
          />
        </main>
      );
    }

    // Results section
    if (activeSection === 'results') {
      if (analysisState.status === 'error' && analysisState.error) {
        return (
          <main className="flex-1 p-6 overflow-hidden relative z-10 flex flex-col">
            <AnalysisError message={analysisState.error} onRetry={runAnalysis} />
          </main>
        );
      }
      if (analysisState.status === 'success' && analysisState.result) {
        return (
          <main className="flex-1 p-6 overflow-y-auto relative z-10 flex flex-col">
            <AnalysisResultSummary
              result={analysisState.result}
              onNavigateToEditor={() => setActiveSection('rtl')}
              onNavigateToReports={() => setActiveSection('reports')}
            />
          </main>
        );
      }
      // Results selected but no analysis run yet
      return (
        <main className="flex-1 p-6 overflow-hidden relative z-10 flex flex-col items-center justify-center">
          <p className="text-slate-700 font-mono text-sm">No analysis results yet. Run verification first.</p>
        </main>
      );
    }

    // Analysis section
    if (activeSection === 'analysis') {
      if (analysisState.status === 'error' && analysisState.error) {
        return (
          <main className="flex-1 p-6 overflow-hidden relative z-10 flex flex-col">
            <AnalysisError message={analysisState.error} onRetry={runAnalysis} />
          </main>
        );
      }
      return (
        <main className="flex-1 p-6 overflow-hidden relative z-10 flex flex-col items-center justify-center">
          <p className="text-slate-700 font-mono text-sm">
            {analysisState.status === 'success'
              ? 'Analysis complete — check Results.'
              : 'Ready to analyze. Use Overview → Start Verification.'}
          </p>
        </main>
      );
    }

    // Default: editor workspace
    return (
      <VerificationWorkspace
        activeSection={activeSection}
        projectState={projectState}
        setProjectState={setProjectState}
        inputStatus={inputStatus}
        onStartVerification={runAnalysis}
      />
    );
  };

  return (
    <div className="h-screen w-screen flex flex-col bg-[#0F1516] text-slate-300 font-sans overflow-hidden">
      <RivaHeader analysisState={analysisState} />

      <div className="flex-1 flex overflow-hidden relative">
        <div className="absolute inset-0 z-0 pointer-events-none opacity-15 riva-bg-glow bg-[radial-gradient(ellipse_at_top_left,_var(--tw-gradient-stops))] from-cyan-900/30 via-[#0F1516] to-[#0F1516]" />

        <Sidebar
          activeSection={activeSection}
          onNavigate={setActiveSection}
          analysisStatus={analysisState.status}
          analysisResult={analysisState.result}
        />

        {renderMain()}

        <ContextPanel
          activeSection={activeSection}
          inputStatus={inputStatus}
          analysisState={analysisState}
        />
      </div>

      <StatusBar analysisState={analysisState} inputStatus={inputStatus} />
    </div>
  );
}
