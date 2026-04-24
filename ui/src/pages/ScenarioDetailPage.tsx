import { ArrowLeft, ArrowRight, Crown } from "lucide-react";
import { useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { RoleCard } from "@/components/scenario/RoleCard";
import { Banner } from "@/components/ui/banner";
import { Button } from "@/components/ui/button";
import { EmptyState } from "@/components/ui/empty-state";
import { Skeleton } from "@/components/ui/skeleton";
import { useApiErrorHandler } from "@/hooks/use-api-error";
import { useCreateConversationMutation } from "@/hooks/use-conversations";
import { useScenarioQuery } from "@/hooks/use-scenarios";
import { useAuth } from "@/providers/AuthProvider";

export function ScenarioDetailPage() {
  const { scenarioId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const handleApiError = useApiErrorHandler();
  const scenarioQuery = useScenarioQuery(scenarioId);
  const createConversationMutation = useCreateConversationMutation();
  const [selectedRoleId, setSelectedRoleId] = useState<string | null>(null);

  const scenario = scenarioQuery.data;
  const locked = Boolean(scenario?.is_premium && user?.plan !== "premium");
  const selectedRole = useMemo(
    () => scenario?.roles.find((role) => role.id === selectedRoleId) ?? null,
    [scenario?.roles, selectedRoleId]
  );
  const oppositeRole = useMemo(
    () => scenario?.roles.find((role) => role.id !== selectedRoleId) ?? null,
    [scenario?.roles, selectedRoleId]
  );

  async function handleStartConversation() {
    if (!scenario || locked || !selectedRole) return;

    try {
      const conversation = await createConversationMutation.mutateAsync({
        scenario_id: scenario.id,
        scenario_role_id: selectedRole.id,
        generate_opening_message: true
      });
      navigate(`/app/conversations/${conversation.id}`);
    } catch (error) {
      handleApiError(error, "Could not create the conversation.");
    }
  }

  if (scenarioQuery.isLoading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-16 w-48" />
        <Skeleton className="h-64 w-full rounded-[28px]" />
        <div className="grid gap-5 md:grid-cols-2">
          <Skeleton className="h-72 w-full rounded-[28px]" />
          <Skeleton className="h-72 w-full rounded-[28px]" />
        </div>
      </div>
    );
  }

  if (scenarioQuery.isError || !scenario) {
    return <EmptyState title="Scenario not found" description="This scenario could not be loaded." actionLabel="Back to scenarios" onAction={() => navigate("/app/scenarios")} />;
  }

  return (
    <div className="space-y-6">
      <Button variant="ghost" onClick={() => navigate("/app/scenarios")}>
        <ArrowLeft className="h-4 w-4" />
        Back to scenarios
      </Button>

      <section className="glass-panel p-8">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
          <div className="max-w-3xl">
            <div className="mb-3 inline-flex rounded-full bg-slate-950 px-4 py-2 text-xs font-semibold uppercase tracking-[0.2em] text-white">
              {scenario.name}
            </div>
            <h1 className="font-display text-5xl text-ink">{scenario.description}</h1>
            <p className="mt-5 text-base leading-8 text-slate-600">{scenario.prompt_context}</p>
          </div>
          <div className="rounded-[28px] bg-white/85 p-5 shadow-sm">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Session structure</p>
            <p className="mt-3 text-sm leading-7 text-slate-600">Choose one role below. The AI automatically plays the other side of the conversation.</p>
            {scenario.is_premium ? (
              <div className="mt-4 inline-flex items-center gap-2 rounded-full bg-amber-100 px-3 py-1 text-sm font-medium text-amber-800">
                <Crown className="h-4 w-4" />
                Premium scenario
              </div>
            ) : null}
          </div>
        </div>
      </section>

      {locked ? (
        <Banner
          tone="warning"
          title="This scenario is visually locked for free plans"
          description="The backend does not enforce premium access yet, but this UI keeps premium scenarios styled as locked unless the learner has a premium plan."
        />
      ) : null}

      {createConversationMutation.isError ? (
        <Banner
          tone="danger"
          title="Conversation could not be created"
          description={createConversationMutation.error instanceof Error ? createConversationMutation.error.message : "Try again in a moment."}
        />
      ) : null}

      <div className="grid gap-5 lg:grid-cols-2">
        {scenario.roles.map((role) => {
          const oppositeRole = scenario.roles.find((candidate) => candidate.id !== role.id);
          return (
            <RoleCard
              key={role.id}
              role={role}
              oppositeRoleName={oppositeRole?.role_name}
              selected={selectedRoleId === role.id}
              onSelect={() => setSelectedRoleId(role.id)}
            />
          );
        })}
      </div>

      <section className="glass-panel flex flex-col gap-4 p-6 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.2em] text-accent">Start conversation</p>
          <h2 className="mt-2 text-2xl font-semibold text-slate-950">
            {selectedRole ? `You will play ${selectedRole.role_name}` : "Choose a role to continue"}
          </h2>
          <p className="mt-2 text-sm leading-7 text-slate-600">
            {selectedRole
              ? `The AI will respond as ${oppositeRole?.role_name ?? "the opposite role"} and can open the roleplay automatically.`
              : "Select one of the two role cards above. The AI will immediately take the opposite perspective."}
          </p>
        </div>
        <Button
          size="lg"
          onClick={handleStartConversation}
          disabled={!selectedRole || locked || createConversationMutation.isPending}
        >
          {createConversationMutation.isPending ? "Starting..." : "Start conversation"}
          <ArrowRight className="h-4 w-4" />
        </Button>
      </section>
    </div>
  );
}
