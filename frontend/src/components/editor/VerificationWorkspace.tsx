import type React from 'react';
import type { ProjectState, InputStatus } from '../../types/state';
import { OverviewTab } from './OverviewTab';
import { EditorToolbar } from './EditorToolbar';

interface VerificationWorkspaceProps {
  activeSection: string;
  projectState: ProjectState;
  setProjectState: React.Dispatch<React.SetStateAction<ProjectState>>;
  inputStatus: InputStatus;
  onStartVerification: () => void;
}

const PLACEHOLDERS: Record<string, string> = {
  specification:
`[REQ-001]
Description: The output y shall represent the sum of a and b.
Signal: y
Expected: 8-bit output
Category: FUNCTIONAL`,
  rtl:
`module top (
    input  logic [7:0] a,
    input  logic [7:0] b,
    output logic [7:0] y
);
    assign y = a + b;
endmodule`,
  testbench:
`module tb;
    logic [7:0] a, b, y;
    top dut (.a(a), .b(b), .y(y));
    initial begin
        a = 8'd10; b = 8'd20;
        #10;
        $display("y=%d", y);
    end
endmodule`,
  waveform:
`$timescale 1ns $end
$var wire 8 ! a [7:0] $end
$var wire 8 " y [7:0] $end
#0
b00001010 !
b00000000 "
#10
b00010100 !
b00011110 "`,
};

const EDITOR_FIELD: Record<string, 'specCode' | 'rtlCode' | 'testbenchCode' | 'vcdContent'> = {
  specification: 'specCode',
  rtl: 'rtlCode',
  testbench: 'testbenchCode',
  waveform: 'vcdContent',
};

const DIRTY_FIELD: Record<string, 'isDirtySpec' | 'isDirtyRtl' | 'isDirtyTb' | 'isDirtyVcd'> = {
  specification: 'isDirtySpec',
  rtl: 'isDirtyRtl',
  testbench: 'isDirtyTb',
  waveform: 'isDirtyVcd',
};

export function VerificationWorkspace({ activeSection, projectState, setProjectState, inputStatus, onStartVerification }: VerificationWorkspaceProps) {

  const isEditor = ['specification', 'rtl', 'testbench', 'waveform'].includes(activeSection);

  const renderContent = () => {
    if (activeSection === 'overview') {
      return <OverviewTab projectState={projectState} inputStatus={inputStatus} onStartVerification={onStartVerification} />;
    }

    if (isEditor) {
      const field = EDITOR_FIELD[activeSection];
      const dirtyField = DIRTY_FIELD[activeSection];
      const value = projectState[field];

      const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        const val = e.target.value;
        setProjectState(prev => ({ ...prev, [field]: val, [dirtyField]: true }));
      };

      return (
        <div className="flex flex-col h-full rounded-xl border border-slate-800 bg-[#0d1117] shadow-[0_4px_30px_rgba(0,0,0,0.6)] overflow-hidden">
          <EditorToolbar
            activeSection={activeSection}
            projectState={projectState}
            setProjectState={setProjectState}
          />
          <textarea
            spellCheck={false}
            value={value}
            onChange={handleChange}
            placeholder={PLACEHOLDERS[activeSection]}
            className="riva-editor flex-1 w-full p-6"
            style={{ height: '100%' }}
            aria-label={`${activeSection} editor`}
          />
        </div>
      );
    }

    return (
      <div className="flex h-full items-center justify-center">
        <p className="text-slate-700 font-mono text-sm">
          Select a section from the sidebar to get started.
        </p>
      </div>
    );
  };

  return (
    <main className="flex-1 p-6 overflow-hidden relative z-10 flex flex-col">
      {renderContent()}
    </main>
  );
}
