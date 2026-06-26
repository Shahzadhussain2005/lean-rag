import axios from "axios";
import type {
  CacheStats,
  Document,
  DocumentListResponse,
  QueryRequest,
  QueryResponse,
} from "@/types/api";
import apiClient from "./apiClient";

export const documentsApi = {
  upload: async (file: File): Promise<Document> => {
    const form = new FormData();
    form.append("file", file);
    const { data } = await apiClient.post<Document>("/documents", form, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return data;
  },

  list: async (): Promise<DocumentListResponse> => {
    const { data } = await apiClient.get<DocumentListResponse>("/documents");
    return data;
  },

  get: async (id: string): Promise<Document> => {
    const { data } = await apiClient.get<Document>(`/documents/${id}`);
    return data;
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/documents/${id}`);
  },
};

export const queryApi = {
  query: async (request: QueryRequest): Promise<QueryResponse> => {
    const { data } = await apiClient.post<QueryResponse>("/query", request);
    return data;
  },
};

export const systemApi = {
  getCacheStats: async (): Promise<CacheStats> => {
    const { data } = await axios.get<CacheStats>("/cache/stats");
    return data;
  },
};
