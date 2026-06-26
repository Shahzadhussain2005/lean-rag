import { useCallback } from "react";
import { queryApi } from "@/services/api";
import { useAppStore, type ChatMessage } from "@/store/appStore";

let _counter = 0;
const genId = () => `msg-${Date.now()}-${++_counter}`;

export function useQuery() {
  const { isQuerying, selectedDocumentId, addMessage, setIsQuerying } = useAppStore();

  const sendQuery = useCallback(
    async (question: string) => {
      const userMsg: ChatMessage = {
        id: genId(),
        role: "user",
        content: question,
        timestamp: new Date(),
      };
      addMessage(userMsg);
      setIsQuerying(true);

      try {
        const result = await queryApi.query({
          question,
          document_id: selectedDocumentId ?? undefined,
        });

        const assistantMsg: ChatMessage = {
          id: genId(),
          role: "assistant",
          content: result.answer,
          sources: result.sources,
          costMetrics: result.cost_metrics,
          cached: result.cached,
          timestamp: new Date(),
        };
        addMessage(assistantMsg);
        return result;
      } catch (err) {
        const errorMsg: ChatMessage = {
          id: genId(),
          role: "assistant",
          content: `Error: ${err instanceof Error ? err.message : "Something went wrong."}`,
          timestamp: new Date(),
        };
        addMessage(errorMsg);
        throw err;
      } finally {
        setIsQuerying(false);
      }
    },
    [selectedDocumentId, addMessage, setIsQuerying]
  );

  return { isQuerying, sendQuery };
}
