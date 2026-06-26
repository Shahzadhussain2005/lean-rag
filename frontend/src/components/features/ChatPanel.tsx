import { useEffect, useRef, useState, type KeyboardEvent } from "react";
import { Send, Trash2, Bot } from "lucide-react";
import { clsx } from "clsx";
import { useAppStore } from "@/store/appStore";
import { useQuery } from "@/hooks/useQuery";
import { MessageBubble } from "./MessageBubble";
import { Spinner } from "@/components/ui/Spinner";

export function ChatPanel() {
  const { messages, clearMessages, selectedDocumentId, documents } = useAppStore();
  const { isQuerying, sendQuery } = useQuery();
  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);

  const selectedDoc = documents.find((d) => d.id === selectedDocumentId);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isQuerying]);

  const handleSend = async () => {
    const q = input.trim();
    if (!q || isQuerying) return;
    setInput("");
    await sendQuery(q);
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between border-b border-gray-800 px-4 py-3">
        <div>
          <h2 className="text-sm font-semibold text-gray-100">Chat</h2>
          {selectedDoc ? (
            <p className="text-xs text-gray-500 mt-0.5">
              Querying <span className="text-brand-400">{selectedDoc.filename}</span>
            </p>
          ) : (
            <p className="text-xs text-gray-500 mt-0.5">All documents</p>
          )}
        </div>
        {messages.length > 0 && (
          <button
            onClick={clearMessages}
            className="btn-ghost text-xs"
            title="Clear conversation"
          >
            <Trash2 className="h-3.5 w-3.5" />
            Clear
          </button>
        )}
      </div>

      <div className="flex-1 overflow-y-auto px-4 py-4">
        {messages.length === 0 ? (
          <div className="flex h-full flex-col items-center justify-center gap-3 text-center">
            <div className="flex h-14 w-14 items-center justify-center rounded-full bg-gray-800">
              <Bot className="h-7 w-7 text-gray-500" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-400">Ask anything about your documents</p>
              <p className="mt-1 text-xs text-gray-600">
                Each response shows real-time cost metrics and source chunks
              </p>
            </div>
            <div className="mt-2 grid grid-cols-1 gap-2 sm:grid-cols-2">
              {["Summarize the main points", "What are the key findings?", "Explain the methodology", "List all conclusions"].map(
                (suggestion) => (
                  <button
                    key={suggestion}
                    onClick={() => setInput(suggestion)}
                    className="rounded-lg border border-gray-800 bg-gray-900 px-3 py-2 text-left text-xs text-gray-400 hover:border-gray-700 hover:text-gray-300 transition-colors"
                  >
                    {suggestion}
                  </button>
                )
              )}
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            {messages.map((msg) => (
              <MessageBubble key={msg.id} message={msg} />
            ))}
            {isQuerying && (
              <div className="flex gap-3">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-gray-800">
                  <Spinner size="sm" />
                </div>
                <div className="flex items-center gap-2 rounded-xl rounded-tl-sm bg-gray-800 px-4 py-3">
                  <span className="text-xs text-gray-400">Thinking…</span>
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>
        )}
      </div>

      <div className="border-t border-gray-800 p-4">
        <div
          className={clsx(
            "flex items-end gap-2 rounded-xl border bg-gray-800 px-3 py-2 transition-colors focus-within:border-brand-500/50",
            "border-gray-700"
          )}
        >
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask a question… (Enter to send, Shift+Enter for newline)"
            rows={1}
            className="flex-1 resize-none bg-transparent text-sm text-gray-100 placeholder-gray-500 focus:outline-none"
            style={{ maxHeight: "120px" }}
            onInput={(e) => {
              const el = e.currentTarget;
              el.style.height = "auto";
              el.style.height = `${el.scrollHeight}px`;
            }}
            disabled={isQuerying}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || isQuerying}
            className={clsx(
              "flex h-8 w-8 shrink-0 items-center justify-center rounded-lg transition-colors",
              input.trim() && !isQuerying
                ? "bg-brand-500 text-white hover:bg-brand-600"
                : "bg-gray-700 text-gray-500 cursor-not-allowed"
            )}
          >
            <Send className="h-4 w-4" />
          </button>
        </div>
        <p className="mt-1.5 text-center text-[10px] text-gray-600">
          Powered by Groq · llama3-8b-8192 · Semantic cache active
        </p>
      </div>
    </div>
  );
}
