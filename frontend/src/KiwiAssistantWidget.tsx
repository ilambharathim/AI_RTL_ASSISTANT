import React, { useState } from 'react';
import { X, Send } from 'lucide-react';

interface Message {
  sender: 'kiwi' | 'user';
  text: string;
}

export const KiwiAssistantWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      sender: 'kiwi',
      text: "KIWI Verification Assistant Ready. I can help guide you through SystemVerilog analysis, bit-width verification rules, or explain diagnostics like RIVA2003 & RIVA6001."
    }
  ]);
  const [input, setInput] = useState('');

  const quickPrompts = [
    "Explain RIVA 9-stage pipeline",
    "How to fix RIVA2003 width mismatch?",
    "Explain specification traceability"
  ];

  const handleSend = (textToSend?: string) => {
    const query = textToSend || input;
    if (!query.trim()) return;

    setMessages(prev => [...prev, { sender: 'user', text: query }]);
    if (!textToSend) setInput('');

    setTimeout(() => {
      let reply = "";
      const lower = query.toLowerCase();
      if (lower.includes("pipeline") || lower.includes("stage") || lower.includes("how")) {
        reply = "RIVA Verification Pipeline:\n1. Spec IR & Normalization\n2. SystemVerilog Lexer & AST Parser\n3. Semantic Symbol Analysis\n4. Hierarchy Elaboration\n5. Control Flow (CFG) & Dataflow Graphs\n6. Diagnostic Rule Engine (RIVA2003/RIVA6001)\n7. Specification Requirement Tracer\n8. Waveform Event Analysis (VCD)\n9. Grounded Evidence AI Engine";
      } else if (lower.includes("width") || lower.includes("riva2003") || lower.includes("mismatch")) {
        reply = "RIVA2003 occurs when a procedural assignment truncates high bits (e.g. data_out[7:0] <- data_in[15:0]). Update your port declaration to logic [15:0] data_out to resolve the width mismatch!";
      } else if (lower.includes("traceability") || lower.includes("spec") || lower.includes("req")) {
        reply = "Requirement Tracer maps [REQ-xxx] definitions from specification.txt against elaborated AST signal declarations and validates expected vs actual bit-widths.";
      } else {
        reply = `Analyzing requirement for '${query}' against active SystemVerilog AST and Dataflow graph. Click '▶ Run Verification' on the left toolbar to refresh pipeline results.`;
      }
      setMessages(prev => [...prev, { sender: 'kiwi', text: reply }]);
    }, 350);
  };

  return (
    <>
      {/* Floating Action Button (FAB) - Bottom Right Corner */}
      {!isOpen && (
        <div className="kiwi-widget-fab">
          <button onClick={() => setIsOpen(true)} className="kiwi-fab-btn">
            <div className="w-5 h-5 rounded bg-cyan-500/20 text-cyan-400 flex items-center justify-center font-bold text-xs">
              🥝
            </div>
            <span>KIWI Assistant</span>
            <span className="w-2 h-2 rounded-full bg-emerald-400" />
          </button>
        </div>
      )}

      {/* Expanded Floating KIWI Workstation Assistant Window */}
      {isOpen && (
        <div className="kiwi-modal-window">
          {/* Header */}
          <div className="p-3 bg-slate-950 border-b border-slate-800 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded bg-cyan-500/20 text-cyan-400 flex items-center justify-center font-bold text-xs">
                🥝
              </div>
              <div>
                <h4 className="text-xs font-bold text-white flex items-center gap-1.5">
                  KIWI Verification Assistant
                  <span className="badge badge-green text-[9px]">Grounded AI</span>
                </h4>
                <p className="text-[10px] text-slate-400">Enterprise Engineering Guide</p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="p-1 rounded text-slate-400 hover:text-white hover:bg-slate-900 transition"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Quick Prompts Bar */}
          <div className="p-2 bg-slate-950/80 border-b border-slate-800/60 flex items-center gap-1 overflow-x-auto">
            {quickPrompts.map((qp, idx) => (
              <button
                key={idx}
                onClick={() => handleSend(qp)}
                className="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-[10px] text-slate-300 hover:text-cyan-400 hover:border-cyan-500/40 whitespace-nowrap transition"
              >
                {qp}
              </button>
            ))}
          </div>

          {/* Messages Body */}
          <div className="flex-1 p-3 overflow-y-auto space-y-2 font-mono text-xs">
            {messages.map((m, idx) => (
              <div
                key={idx}
                className={`p-2.5 rounded-lg whitespace-pre-wrap leading-relaxed ${
                  m.sender === 'user'
                    ? 'bg-cyan-500 text-slate-950 font-medium ml-4'
                    : 'bg-slate-900 border border-slate-800 text-slate-200 mr-4'
                }`}
              >
                {m.text}
              </div>
            ))}
          </div>

          {/* Prompt Bar */}
          <div className="p-2.5 bg-slate-950 border-t border-slate-800 flex items-center gap-2">
            <input
              type="text"
              placeholder="Ask KIWI verification assistant..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              className="flex-1 bg-slate-900 border border-slate-800 rounded px-3 py-1.5 text-xs text-white focus:outline-none focus:border-cyan-400 font-mono"
            />
            <button
              onClick={() => handleSend()}
              className="p-1.5 rounded bg-cyan-500 text-slate-950 hover:bg-cyan-400 transition"
            >
              <Send className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}
    </>
  );
};
