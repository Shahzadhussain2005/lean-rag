import { useState } from "react";
import { ChevronDown, ChevronRight } from "lucide-react";
import type { SourceChunk } from "@/types/api";

interface SourcesAccordionProps {
  sources: SourceChunk[];
}

export function SourcesAccordion({ sources }: SourcesAccordionProps) {
  const [open, setOpen] = useState(false);

  if (sources.length === 0) return null;

  return (
    <div className="mt-2">
      <button
        onClick={() => setOpen((v) => !v)}
        className="flex items-center gap-1.5 text-xs text-gray-500 hover:text-gray-300 transition-colors"
      >
        {open ? <ChevronDown className="h-3.5 w-3.5" /> : <ChevronRight className="h-3.5 w-3.5" />}
        {sources.length} source{sources.length !== 1 ? "s" : ""}
      </button>

      {open && (
        <ul className="mt-2 space-y-2">
          {sources.map((src, i) => (
            <li key={src.chunk_id} className="rounded-lg border border-gray-800 bg-gray-900/50 px-3 py-2">
              <div className="mb-1 flex items-center justify-between gap-2">
                <span className="text-[10px] font-semibold uppercase tracking-widest text-gray-500">
                  Source {i + 1} · chunk #{src.chunk_index}
                </span>
                <span className="text-[10px] font-mono text-brand-400">
                  {(src.score * 100).toFixed(1)}% match
                </span>
              </div>
              <p className="line-clamp-4 text-xs text-gray-400 leading-relaxed">{src.text}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
