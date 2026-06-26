import { Zap, Database, Scissors, TrendingDown } from "lucide-react";
import type { CostMetrics } from "@/types/api";
import { Tooltip } from "@/components/ui/Tooltip";

interface CostMetricsPanelProps {
  metrics: CostMetrics;
  cached: boolean;
}

interface StatItem {
  icon: React.ReactNode;
  label: string;
  value: string;
  tooltip: string;
}

export function CostMetricsPanel({ metrics, cached }: CostMetricsPanelProps) {
  const stats: StatItem[] = [
    {
      icon: <Zap className="h-3.5 w-3.5" />,
      label: "Tokens",
      value: cached ? "0 (cached)" : String(metrics.total_tokens),
      tooltip: `Prompt: ${metrics.prompt_tokens} · Completion: ${metrics.completion_tokens}`,
    },
    {
      icon: <Database className="h-3.5 w-3.5" />,
      label: "Chunks used",
      value: String(metrics.chunks_retrieved),
      tooltip: "Number of document chunks sent as context to the LLM",
    },
    {
      icon: <Scissors className="h-3.5 w-3.5" />,
      label: "Query compressed",
      value: metrics.query_compressed ? "Yes" : "No",
      tooltip: "Query was rewritten to a shorter keyword form before retrieval",
    },
    {
      icon: <TrendingDown className="h-3.5 w-3.5" />,
      label: "Est. savings",
      value: `${metrics.estimated_savings_pct}%`,
      tooltip: "Estimated token savings vs. a naive full-context approach",
    },
  ];

  return (
    <div className="mt-2 rounded-lg border border-gray-800 bg-gray-900/60 px-3 py-2">
      <p className="mb-2 text-[10px] font-semibold uppercase tracking-widest text-gray-500">
        Cost Metrics
      </p>
      <div className="grid grid-cols-2 gap-x-4 gap-y-1.5 sm:grid-cols-4">
        {stats.map((s) => (
          <Tooltip key={s.label} content={s.tooltip}>
            <div className="flex items-center gap-1.5 cursor-default">
              <span className="text-gray-500">{s.icon}</span>
              <div>
                <p className="text-[10px] text-gray-500">{s.label}</p>
                <p className="text-xs font-semibold text-gray-200">{s.value}</p>
              </div>
            </div>
          </Tooltip>
        ))}
      </div>
    </div>
  );
}
