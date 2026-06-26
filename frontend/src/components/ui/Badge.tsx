import { clsx } from "clsx";
import type { ReactNode } from "react";

type Variant = "default" | "success" | "warning" | "danger" | "info" | "purple";

const variantMap: Record<Variant, string> = {
  default: "bg-gray-800 text-gray-300",
  success: "bg-emerald-900/50 text-emerald-400",
  warning: "bg-amber-900/50 text-amber-400",
  danger: "bg-red-900/50 text-red-400",
  info: "bg-brand-900/50 text-brand-300",
  purple: "bg-purple-900/50 text-purple-400",
};

interface BadgeProps {
  children: ReactNode;
  variant?: Variant;
  className?: string;
}

export function Badge({ children, variant = "default", className }: BadgeProps) {
  return (
    <span className={clsx("badge", variantMap[variant], className)}>{children}</span>
  );
}
