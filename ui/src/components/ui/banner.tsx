import { AlertTriangle, CheckCircle2, Info } from "lucide-react";

import { cn } from "@/lib/utils";

const styles = {
  info: {
    wrapper: "border-cyan-200 bg-cyan-50/90 text-cyan-900",
    icon: Info
  },
  success: {
    wrapper: "border-emerald-200 bg-emerald-50/90 text-emerald-900",
    icon: CheckCircle2
  },
  warning: {
    wrapper: "border-orange-200 bg-orange-50/90 text-orange-900",
    icon: AlertTriangle
  },
  danger: {
    wrapper: "border-rose-200 bg-rose-50/90 text-rose-900",
    icon: AlertTriangle
  }
} as const;

export function Banner({
  tone = "info",
  title,
  description,
  className
}: {
  tone?: keyof typeof styles;
  title: string;
  description?: string;
  className?: string;
}) {
  const Icon = styles[tone].icon;

  return (
    <div className={cn("flex items-start gap-3 rounded-3xl border px-4 py-3 shadow-sm", styles[tone].wrapper, className)}>
      <Icon className="mt-0.5 h-5 w-5 shrink-0" />
      <div>
        <p className="font-medium">{title}</p>
        {description ? <p className="mt-1 text-sm opacity-90">{description}</p> : null}
      </div>
    </div>
  );
}
