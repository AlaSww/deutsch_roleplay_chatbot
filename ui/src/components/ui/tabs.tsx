import { cn } from "@/lib/utils";

export function Tabs({
  tabs,
  value,
  onValueChange
}: {
  tabs: { label: string; value: string }[];
  value: string;
  onValueChange: (value: string) => void;
}) {
  return (
    <div className="inline-flex rounded-full border border-white/70 bg-white/80 p-1 shadow-sm">
      {tabs.map((tab) => (
        <button
          key={tab.value}
          type="button"
          className={cn(
            "rounded-full px-4 py-2 text-sm font-medium transition",
            value === tab.value ? "bg-slate-950 text-white" : "text-slate-600 hover:text-slate-900"
          )}
          onClick={() => onValueChange(tab.value)}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}
