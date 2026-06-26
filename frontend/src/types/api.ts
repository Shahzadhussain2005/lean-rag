export type DocumentStatus = "processing" | "ready" | "failed";

export interface Document {
  id: string;
  filename: string;
  content_type: string;
  status: DocumentStatus;
  created_at: string;
  chunk_count: number;
  total_tokens: number;
  error_message?: string;
}

export interface DocumentListResponse {
  documents: Document[];
  total: number;
}

export interface SourceChunk {
  chunk_id: string;
  document_id: string;
  text: string;
  score: number;
  chunk_index: number;
}

export interface CostMetrics {
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
  cache_hit: boolean;
  chunks_retrieved: number;
  query_compressed: boolean;
  estimated_savings_pct: number;
}

export interface QueryResponse {
  answer: string;
  sources: SourceChunk[];
  cost_metrics: CostMetrics;
  cached: boolean;
}

export interface CacheStats {
  total_entries: number;
  hit_count: number;
  miss_count: number;
  hit_rate_pct: number;
  estimated_tokens_saved: number;
}

export interface QueryRequest {
  question: string;
  document_id?: string;
  top_k?: number;
}
