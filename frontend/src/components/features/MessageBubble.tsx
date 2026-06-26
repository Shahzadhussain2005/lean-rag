import ReactMarkdown from "react-markdown";
import { clsx } from "clsx";
import { Bot, User, Sparkles } from "lucide-react";
import type { ChatMessage } from "@/store/appStore";
import { Badge } from "@/components/ui/Badge";
import { CostMetricsPanel } from "./CostMetricsPanel";
import { SourcesAccordion } from "./SourcesAccordion";

interface MessageBubbleProps {
  message: ChatMessage;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";

  return (
    <div className={clsx("flex gap-3", isUser && "flex-row-reverse")}>
      <div
        className={clsx(
          "flex h-8 w-8 shrink-0 items-center justify-center rounded-full",
          isUser ? "bg-brand-500/20" : "bg-gray-800"
        )}
      >
        {isUser ? (
          <User className="h-4 w-4 text-brand-400" />
        ) : (
          <Bot className="h-4 w-4 text-gray-400" />
        )}
      </div>

      <div className={clsx("min-w-0 max-w-[85%]", isUser && "items-end flex flex-col")}>
        {message.cached && (
          <div className="mb-1 flex justify-start">
            <Badge variant="purple">
              <Sparkles className="h-3 w-3" />
              Cached response
            </Badge>
          </div>
        )}

        <div
          className={clsx(
            "rounded-xl px-4 py-3 text-sm leading-relaxed",
            isUser
              ? "bg-brand-500/15 text-gray-100 rounded-tr-sm"
              : "bg-gray-800 text-gray-200 rounded-tl-sm"
          )}
        >
          {isUser ? (
            <p>{message.content}</p>
          ) : (
            <div className="prose prose-sm prose-invert max-w-none prose-p:my-1 prose-pre:bg-gray-900 prose-code:text-brand-300">
              <ReactMarkdown>{message.content}</ReactMarkdown>
            </div>
          )}
        </div>

        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="mt-1 w-full">
            <SourcesAccordion sources={message.sources} />
          </div>
        )}

        {!isUser && message.costMetrics && (
          <div className="mt-1 w-full">
            <CostMetricsPanel metrics={message.costMetrics} cached={message.cached ?? false} />
          </div>
        )}

        <p className="mt-1 px-1 text-[10px] text-gray-600">
          {message.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
        </p>
      </div>
    </div>
  );
}
