import { BarChart3 } from "lucide-react";
import { useDocuments } from "@/hooks/useDocuments";
import { useAppStore } from "@/store/appStore";
import { UploadZone } from "@/components/features/UploadZone";
import { DocumentList } from "@/components/features/DocumentList";

export function Sidebar() {
  const { documents, isUploading, uploadDocument, deleteDocument } = useDocuments();
  const { selectedDocumentId, selectDocument } = useAppStore();

  return (
    <aside className="flex h-full w-72 shrink-0 flex-col border-r border-gray-800 bg-gray-950">
      <div className="flex items-center gap-2.5 border-b border-gray-800 px-4 py-4">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-500/20">
          <BarChart3 className="h-4 w-4 text-brand-400" />
        </div>
        <div>
          <h1 className="text-sm font-bold text-gray-100">RAG Studio</h1>
          <p className="text-[10px] text-gray-500">Cost-optimized retrieval</p>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        <UploadZone onUpload={uploadDocument} isUploading={isUploading} />

        <div>
          <div className="mb-2 flex items-center justify-between">
            <h2 className="text-xs font-semibold uppercase tracking-widest text-gray-500">
              Documents
            </h2>
            <span className="text-xs text-gray-600">{documents.length}</span>
          </div>
          <DocumentList
            documents={documents}
            selectedId={selectedDocumentId}
            onSelect={selectDocument}
            onDelete={deleteDocument}
          />
        </div>
      </div>

      <div className="border-t border-gray-800 px-4 py-3">
        <div className="rounded-lg bg-gray-900 px-3 py-2.5">
          <p className="mb-1.5 text-[10px] font-semibold uppercase tracking-widest text-gray-500">
            Cost Optimizations Active
          </p>
          <ul className="space-y-1">
            {[
              "Semantic response cache",
              "Query compression",
              "Token-budget context trim",
              "Sentence-aware chunking",
            ].map((opt) => (
              <li key={opt} className="flex items-center gap-2 text-xs text-gray-400">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 shrink-0" />
                {opt}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </aside>
  );
}
