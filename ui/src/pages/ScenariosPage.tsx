import { Search } from "lucide-react";
import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import { ScenarioCard } from "@/components/scenario/ScenarioCard";
import { EmptyState } from "@/components/ui/empty-state";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { Tabs } from "@/components/ui/tabs";
import { useScenariosQuery } from "@/hooks/use-scenarios";
import { useAuth } from "@/providers/AuthProvider";

type FilterValue = "all" | "free" | "premium";

export function ScenariosPage() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState<FilterValue>("all");
  const scenariosQuery = useScenariosQuery();

  const scenarios = useMemo(() => {
    const items = scenariosQuery.data ?? [];
    return items.filter((scenario) => {
      if (filter === "free" && scenario.is_premium) return false;
      if (filter === "premium" && !scenario.is_premium) return false;
      if (!search.trim()) return true;
      const haystack = `${scenario.name} ${scenario.description ?? ""} ${scenario.roles.map((role) => role.role_name).join(" ")}`.toLowerCase();
      return haystack.includes(search.trim().toLowerCase());
    });
  }, [scenariosQuery.data, search, filter]);

  return (
    <div className="space-y-6">
      <section className="glass-panel p-8">
        <p className="text-sm uppercase tracking-[0.2em] text-accent">Scenario discovery</p>
        <div className="mt-3 flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <h1 className="font-display text-5xl text-ink">Choose a roleplay that matches your next speaking goal.</h1>
            <p className="mt-4 max-w-3xl text-base leading-8 text-slate-600">
              Browse practical German situations, choose the role you want to play, and let the AI handle the
              other perspective naturally.
            </p>
          </div>
          <div className="rounded-3xl bg-white/80 px-5 py-4 text-sm text-slate-600 shadow-sm">
            Logged in as <span className="font-semibold text-slate-950">{user?.plan}</span>. Premium scenarios are
            visually gated client-side.
          </div>
        </div>
      </section>

      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div className="relative max-w-xl flex-1">
          <Search className="pointer-events-none absolute left-4 top-3.5 h-5 w-5 text-slate-400" />
          <Input className="pl-12" placeholder="Search cafe, interview, doctor..." value={search} onChange={(e) => setSearch(e.target.value)} />
        </div>
        <Tabs
          tabs={[
            { label: "All", value: "all" },
            { label: "Free", value: "free" },
            { label: "Premium", value: "premium" }
          ]}
          value={filter}
          onValueChange={(value) => setFilter(value as FilterValue)}
        />
      </div>

      {scenariosQuery.isLoading ? (
        <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
          {Array.from({ length: 6 }).map((_, index) => (
            <div key={index} className="rounded-[28px] border border-white/60 bg-white/70 p-6 shadow-glass">
              <Skeleton className="h-6 w-24" />
              <Skeleton className="mt-5 h-8 w-2/3" />
              <Skeleton className="mt-3 h-20 w-full" />
              <div className="mt-5 flex gap-2">
                <Skeleton className="h-7 w-20 rounded-full" />
                <Skeleton className="h-7 w-24 rounded-full" />
              </div>
              <Skeleton className="mt-6 h-11 w-full rounded-full" />
            </div>
          ))}
        </div>
      ) : scenariosQuery.isError ? (
        <EmptyState
          title="Could not load scenarios"
          description={scenariosQuery.error instanceof Error ? scenariosQuery.error.message : "Try again in a moment."}
          actionLabel="Retry"
          onAction={() => scenariosQuery.refetch()}
        />
      ) : scenarios.length === 0 ? (
        <EmptyState
          title="No scenarios match this filter"
          description="Try a different search term or switch between all, free, and premium."
        />
      ) : (
        <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
          {scenarios.map((scenario) => (
            <ScenarioCard
              key={scenario.id}
              scenario={scenario}
              locked={scenario.is_premium && user?.plan !== "premium"}
              onOpen={() => navigate(`/app/scenarios/${scenario.id}`)}
            />
          ))}
        </div>
      )}
    </div>
  );
}
