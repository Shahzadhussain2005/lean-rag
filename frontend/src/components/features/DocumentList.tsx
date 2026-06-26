import { FileText, Trash2, CheckCircle2, AlertCircle, Loader2 } from "lucide-react";
import { clsx } from "clsx";
import type { Document } from "@/types/api";
import { Badge } from "@/components/ui/Badge";
import { Tooltip } from "@/components/ui/Tooltip";

interface DocumentListProps {
  documents: Document[];
  selectedId: string | null;
  onSelect: (id: string | null) => void;
  onDelete: (id: string) => void;
}

const statusIcon = {
  ready: <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400" />,
  processing: <Loader2 className="h-3.5 w-3.5 text-amber-400 animate-spin" />,
  failed: <AlertCircle className="h-3.5 w-3.5 text-red-400" />,
};

const statusVariant = { ready: "success", processing: "warning", failed: "danger" } as const;

function formatBytes(n: number): string {
  return n > 1000 ? `${(n / 1000).toFixed(1)}k` : String(n);
}

export function DocumentList({ documents, selectedId, onSelect, onDelete }: DocumentListProps) {
  if (documents.length === 0) {
    return (
      <p className="py-6 text-center text-xs text-gray-500">No documents yet. Upload one above.</p>
    );
  }

  return (
    <ul className="space-y-1.5">
      {documents.map((doc) => (
        <li key={doc.id}>
          <button
            onClick={() => onSelect(selectedId === doc.id ? null : doc.id)}
            className={clsx(
              "group w-full flex items-start gap-3 rounded-lg px-3 py-2.5 text-left transition-colors",
              selectedId === doc.id
                ? "bg-brand-500/10 border border-brand-500/30"
                : "hover:bg-gray-800 border border-transparent"
            )}
          >
            <FileText
              className={clsx(
                "mt-0.5 h-4 w-4 shrink-0",
                selectedId === doc.id ? "text-brand-400" : "text-gray-500"
              )}
            />
            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-medium text-gray-200">{doc.filename}</p>
              <div className="mt-1 flex flex-wrap items-center gap-1.5">
                <Badge variant={statusVariant[doc.status]}>
                  {statusIcon[doc.status]}
                  {doc.status}
                </Badge>
                {doc.status === "ready" && (
                  <>
                    <span className="text-xs text-gray-500">{doc.chunk_count} chunks</span>
                    <span className="text-xs text-gray-500">·</span>
                    <span className="text-xs text-gray-500">{formatBytes(doc.total_tokens)} tokens</span>
                  </>
                )}
              </div>
              {doc.error_message && (
                <p className="mt-1 truncate text-xs text-red-400">{doc.error_message}</p>
              )}
            </div>
            <Tooltip content="Delete document">
              <span
                role="button"
                onClick={(e) => {
                  e.stopPropagation();
                  onDelete(doc.id);
                }}
                className="mt-0.5 shrink-0 rounded p-1 text-gray-600 opacity-0 transition-opacity hover:bg-red-900/40 hover:text-red-400 group-hover:opacity-100"
              >
                <Trash2 className="h-3.5 w-3.5" />
              </span>
            </Tooltip>
          </button>
        </li>
      ))}
    </ul>
  );
}
