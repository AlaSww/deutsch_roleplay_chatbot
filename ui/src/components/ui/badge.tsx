import type { HTMLAttributes } from "react";

import { cn } from "@/lib/utils";

const toneMap = {
  default: "bg-slate-100 text-slate-700",
  success: "bg-emerald-100 text-emerald-700",
  premium: "bg-amber-100 text-amber-800",
  warning: "bg-orange-100 text-orange-800",
  accent: "bg-cyan-100 text-cyan-800",
  danger: "bg-rose-100 text-rose-800"
} as const;

export function Badge({
  className,
  tone = "default",
  ...props
}: HTMLAttributes<HTMLSpanElement> & { tone?: keyof typeof toneMap }) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold tracking-wide",
        toneMap[tone],
        className
      )}
      {...props}
    />
  );
}
