import { useNavigate } from "react-router-dom";

import { StatusBadge } from "@/components/chat/StatusBadge";
import { EmptyState } from "@/components/ui/empty-state";
import { Skeleton } from "@/components/ui/skeleton";
import { useConversationsQuery } from "@/hooks/use-conversations";
import { formatDateTime } from "@/lib/utils";

export function HistoryPage() {
  const navigate = useNavigate();
  const conversationsQuery = useConversationsQuery();

  return (
    <div className="space-y-6">
      <section className="glass-panel p-8">
        <p className="text-sm uppercase tracking-[0.2em] text-accent">Conversation history</p>
        <h1 className="mt-3 font-display text-5xl text-ink">Review past sessions and reopen completed lessons.</h1>
        <p className="mt-4 max-w-2xl text-base leading-8 text-slate-600">
          Active conversations can continue where you left off. Completed conversations open in read-only mode with
          their stored feedback and learner profile updates.
        </p>
      </section>

      {conversationsQuery.isLoading ? (
        <div className="grid gap-4">
          {Array.from({ length: 5 }).map((_, index) => (
            <Skeleton key={index} className="h-32 w-full rounded-[28px]" />
          ))}
        </div>
      ) : conversationsQuery.isError ? (
        <EmptyState
          title="Could not load your conversations"
          description={conversationsQuery.error instanceof Error ? conversationsQuery.error.message : "Try again shortly."}
          actionLabel="Retry"
          onAction={() => conversationsQuery.refetch()}
        />
      ) : !conversationsQuery.data?.length ? (
        <EmptyState title="No conversations yet" description="Start a scenario to create your first AI-powered roleplay session." actionLabel="Browse scenarios" onAction={() => navigate("/app/scenarios")} />
      ) : (
        <div className="grid gap-4">
          {conversationsQuery.data.map((conversation) => (
            <button
              key={conversation.id}
              className="glass-panel flex flex-col items-start gap-4 p-6 text-left transition hover:-translate-y-0.5 hover:shadow-soft lg:flex-row lg:items-center lg:justify-between"
              onClick={() => navigate(`/app/conversations/${conversation.id}`)}
              type="button"
            >
              <div>
                <div className="flex flex-wrap items-center gap-3">
                  <h3 className="text-xl font-semibold text-slate-950">{conversation.scenario_name}</h3>
                  <StatusBadge status={conversation.status} />
                </div>
                <p className="mt-2 text-sm leading-7 text-slate-600">
                  You played <span className="font-medium text-slate-900">{conversation.user_role_name}</span>. AI
                  played <span className="font-medium text-slate-900">{conversation.ai_role_name ?? "the opposite role"}</span>.
                </p>
              </div>
                <div className="grid gap-1 text-sm text-slate-500">
                  <span>{formatDateTime(conversation.started_at)}</span>
                  <span>{conversation.user_message_count} learner messages</span>
                </div>
              </button>
            ))}
        </div>
      )}
    </div>
  );
}
