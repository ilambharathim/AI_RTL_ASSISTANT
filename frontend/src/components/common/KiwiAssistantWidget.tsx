import { useState, useRef, useEffect } from 'react';
import { X, Send, Copy, Check, Loader2, Code, Cpu } from 'lucide-react';
import type { AnalysisState, ProjectState } from '../../types/state';
import { ApiService } from '../../services/api/apiService';

interface KiwiAssistantWidgetProps {
  analysisState?: AnalysisState;
  projectState?: ProjectState;
}

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  provider?: string;
}

export function KiwiAssistantWidget({ analysisState, projectState }: KiwiAssistantWidgetProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: 'assistant',
      content: "Hey! I'm Kiwi — your RIVA Engineering Assistant & Verification Mentor. Ask me why a diagnostic triggered, how to fix bit-widths, or request corrected SystemVerilog code!",
      provider: 'riva_grounded_engine',
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [activeProvider, setActiveProvider] = useState<string>('riva_grounded_engine');
  const [copiedIdx, setCopiedIdx] = useState<number | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const quickPrompts = [
    "Why is my design failing?",
    "What should I fix first?",
    "Give me corrected code",
    "Explain RIVA3001",
    "What is signedness?",
  ];

  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isOpen]);

  const handleSend = async (textToSend?: string) => {
    const query = textToSend || input;
    if (!query.trim() || isLoading) return;

    const newMessages: ChatMessage[] = [...messages, { role: 'user', content: query }];
    setMessages(newMessages);
    if (!textToSend) setInput('');
    setIsLoading(true);

    const projectContext = {
      rtl_code: projectState?.rtlCode || '',
      spec_code: projectState?.specCode || '',
      testbench_code: projectState?.testbenchCode || '',
      vcd_content: projectState?.vcdContent || '',
      result: analysisState?.result || null,
    };

    try {
      const response = await ApiService.kiwiChat({
        messages: newMessages.map(m => ({ role: m.role, content: m.content })),
        project_context: projectContext,
      });

      setActiveProvider(response.provider);
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: response.text,
          provider: response.provider,
        }
      ]);
    } catch {
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: "Unable to process turn with Kiwi assistant backend service.",
          provider: 'offline',
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopyCode = (codeText: string, idx: number) => {
    navigator.clipboard.writeText(codeText);
    setCopiedIdx(idx);
    setTimeout(() => setCopiedIdx(null), 2000);
  };

  const renderMessageContent = (content: string, msgIdx: number) => {
    // Check if message contains code block ```systemverilog ... ```
    const codeBlockMatch = content.match(/```(?:systemverilog|verilog)?\n([\s\S]*?)```/);

    if (codeBlockMatch) {
      const codeSnippet = codeBlockMatch[1].trim();
      const textBefore = content.split(/```(?:systemverilog|verilog)?/)[0].trim();
      const textAfter = content.split(/```/)[2]?.trim();

      return (
        <div className="space-y-2.5 font-sans">
          {textBefore && <p className="leading-relaxed whitespace-pre-wrap">{textBefore}</p>}

          <div className="bg-[#0d1117] rounded-lg border border-slate-800 overflow-hidden font-mono text-xs my-2">
            <div className="px-3 py-1.5 bg-slate-950/80 border-b border-slate-800 flex items-center justify-between">
              <span className="text-[10px] font-bold text-cyan-400 flex items-center gap-1.5">
                <Code className="w-3 h-3 text-cyan-400" />
                Recommended SystemVerilog Correction
              </span>
              <button
                type="button"
                onClick={() => handleCopyCode(codeSnippet, msgIdx)}
                className="flex items-center gap-1 text-[10px] text-slate-400 hover:text-emerald-400 transition"
              >
                {copiedIdx === msgIdx ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                <span>{copiedIdx === msgIdx ? 'Copied!' : 'Copy Code'}</span>
              </button>
            </div>
            <pre className="p-3 text-emerald-300 bg-emerald-950/20 overflow-x-auto leading-relaxed">
              {codeSnippet}
            </pre>
          </div>

          {textAfter && <p className="leading-relaxed whitespace-pre-wrap">{textAfter}</p>}
        </div>
      );
    }

    return <p className="whitespace-pre-wrap leading-relaxed font-sans">{content}</p>;
  };

  return (
    <>
      {/* Floating Action Button (FAB) */}
      {!isOpen && (
        <div className="fixed bottom-9 right-6 z-50">
          <button
            type="button"
            onClick={() => setIsOpen(true)}
            className="flex items-center gap-2 px-3.5 py-2 rounded-full bg-slate-900 border border-cyan-500/40 text-slate-200 text-xs font-semibold shadow-[0_0_20px_rgba(34,211,238,0.15)] hover:border-cyan-400 hover:text-cyan-300 transition-all duration-150 focus-visible:ring-2 focus-visible:ring-cyan-500"
          >
            <div className="w-5 h-5 rounded-full bg-cyan-950 flex items-center justify-center text-xs">
              🥝
            </div>
            <span>Kiwi Assistant</span>
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          </button>
        </div>
      )}

      {/* Expanded KIWI Assistant Window */}
      {isOpen && (
        <div className="fixed bottom-9 right-6 w-[420px] h-[520px] bg-[#0B0F10] border border-slate-800 rounded-xl shadow-2xl z-50 flex flex-col overflow-hidden font-sans">
          {/* Header */}
          <div className="p-3.5 bg-slate-950 border-b border-slate-800/80 flex items-center justify-between flex-shrink-0">
            <div className="flex items-center gap-2.5">
              <div className="w-7 h-7 rounded-lg bg-cyan-950 border border-cyan-800/60 text-cyan-400 flex items-center justify-center text-sm">
                🥝
              </div>
              <div>
                <h4 className="text-xs font-bold text-slate-100 flex items-center gap-2">
                  KIWI — RIVA Assistant
                  <span className="text-[9px] font-mono font-semibold px-1.5 py-0.5 rounded bg-emerald-950/60 text-emerald-400 border border-emerald-800/50 flex items-center gap-1">
                    <Cpu className="w-2.5 h-2.5" />
                    {activeProvider === 'gemini' ? 'Gemini Live' : 'Grounded Engine'}
                  </span>
                </h4>
                <p className="text-[10px] text-slate-500 font-mono">SystemVerilog Engineering Guide</p>
              </div>
            </div>
            <button
              type="button"
              onClick={() => setIsOpen(false)}
              className="p-1 rounded text-slate-500 hover:text-slate-300 hover:bg-slate-900 transition"
              aria-label="Close Kiwi Assistant"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Quick Prompts Bar */}
          <div className="p-2 bg-slate-950/60 border-b border-slate-800/60 flex items-center gap-1.5 overflow-x-auto flex-shrink-0">
            {quickPrompts.map((qp, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => handleSend(qp)}
                disabled={isLoading}
                className="px-2 py-1 rounded bg-slate-900 border border-slate-800 text-[10px] font-mono text-slate-400 hover:text-cyan-300 hover:border-cyan-800/60 whitespace-nowrap transition disabled:opacity-50"
              >
                {qp}
              </button>
            ))}
          </div>

          {/* Messages Body */}
          <div className="flex-1 p-3 overflow-y-auto space-y-3 font-mono text-xs">
            {messages.map((m, idx) => (
              <div
                key={idx}
                className={`p-3 rounded-lg text-xs leading-relaxed ${
                  m.role === 'user'
                    ? 'bg-cyan-950/80 text-cyan-200 border border-cyan-800/60 ml-6 font-sans'
                    : 'bg-slate-900/90 border border-slate-800 text-slate-200 mr-4'
                }`}
              >
                {renderMessageContent(m.content, idx)}
              </div>
            ))}

            {isLoading && (
              <div className="flex items-center gap-2 p-3 rounded-lg bg-slate-900/60 border border-slate-800/80 text-slate-400 text-xs font-mono mr-4">
                <Loader2 className="w-3.5 h-3.5 animate-spin text-cyan-400" />
                <span>Kiwi is analyzing active RIVA project context...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Prompt Input Bar */}
          <div className="p-2.5 bg-slate-950 border-t border-slate-800 flex items-center gap-2 flex-shrink-0">
            <input
              type="text"
              placeholder="Ask Kiwi about RTL diagnostics or SystemVerilog..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              disabled={isLoading}
              className="flex-1 bg-slate-900 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 font-sans placeholder:text-slate-600 disabled:opacity-50"
            />
            <button
              type="button"
              onClick={() => handleSend()}
              disabled={isLoading || !input.trim()}
              className="p-2 rounded-lg bg-cyan-900/60 text-cyan-300 border border-cyan-700/60 hover:bg-cyan-800/60 transition disabled:opacity-50"
              aria-label="Send message"
            >
              <Send className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}
    </>
  );
}
