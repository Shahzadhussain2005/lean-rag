import { useCallback, useEffect } from "react";
import { documentsApi } from "@/services/api";
import { useAppStore } from "@/store/appStore";

export function useDocuments() {
  const { documents, isUploading, setDocuments, addDocument, removeDocument, setIsUploading } =
    useAppStore();

  const fetchDocuments = useCallback(async () => {
    const { documents: docs } = await documentsApi.list();
    setDocuments(docs);
  }, [setDocuments]);

  useEffect(() => {
    fetchDocuments();
  }, [fetchDocuments]);

  const uploadDocument = useCallback(
    async (file: File) => {
      setIsUploading(true);
      try {
        const doc = await documentsApi.upload(file);
        addDocument(doc);

        if (doc.status === "processing") {
          pollUntilReady(doc.id);
        }
        return doc;
      } finally {
        setIsUploading(false);
      }
    },
    [addDocument, setIsUploading]
  );

  const deleteDocument = useCallback(
    async (id: string) => {
      await documentsApi.delete(id);
      removeDocument(id);
    },
    [removeDocument]
  );

  const pollUntilReady = (id: string) => {
    const { updateDocument } = useAppStore.getState();
    const interval = setInterval(async () => {
      try {
        const doc = await documentsApi.get(id);
        updateDocument(doc);
        if (doc.status !== "processing") clearInterval(interval);
      } catch {
        clearInterval(interval);
      }
    }, 2000);
  };

  return { documents, isUploading, uploadDocument, deleteDocument, refetch: fetchDocuments };
}
