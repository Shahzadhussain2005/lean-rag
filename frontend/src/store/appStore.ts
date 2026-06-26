import { create } from "zustand";
import type { CacheStats, Document, QueryResponse, SourceChunk } from "@/types/api";

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: SourceChunk[];
  costMetrics?: QueryResponse["cost_metrics"];
  cached?: boolean;
  timestamp: Date;
}

interface AppState {
  documents: Document[];
  selectedDocumentId: string | null;
  messages: ChatMessage[];
  isQuerying: boolean;
  isUploading: boolean;
  cacheStats: CacheStats | null;

  setDocuments: (docs: Document[]) => void;
  addDocument: (doc: Document) => void;
  removeDocument: (id: string) => void;
  updateDocument: (doc: Document) => void;
  selectDocument: (id: string | null) => void;
  addMessage: (msg: ChatMessage) => void;
  setIsQuerying: (v: boolean) => void;
  setIsUploading: (v: boolean) => void;
  setCacheStats: (stats: CacheStats) => void;
  clearMessages: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  documents: [],
  selectedDocumentId: null,
  messages: [],
  isQuerying: false,
  isUploading: false,
  cacheStats: null,

  setDocuments: (docs) => set({ documents: docs }),
  addDocument: (doc) => set((s) => ({ documents: [doc, ...s.documents] })),
  removeDocument: (id) => set((s) => ({ documents: s.documents.filter((d) => d.id !== id) })),
  updateDocument: (doc) =>
    set((s) => ({ documents: s.documents.map((d) => (d.id === doc.id ? doc : d)) })),
  selectDocument: (id) => set({ selectedDocumentId: id }),
  addMessage: (msg) => set((s) => ({ messages: [...s.messages, msg] })),
  setIsQuerying: (v) => set({ isQuerying: v }),
  setIsUploading: (v) => set({ isUploading: v }),
  setCacheStats: (stats) => set({ cacheStats: stats }),
  clearMessages: () => set({ messages: [] }),
}));

export type { ChatMessage };
