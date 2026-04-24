import { ArrowLeft, LoaderCircle, MessageSquareOff, Sparkles } from "lucide-react";
import { useMemo, useRef } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { ChatBubble } from "@/components/chat/ChatBubble";
import { StatusBadge } from "@/components/chat/StatusBadge";
import { FeedbackCard } from "@/components/feedback/FeedbackCard";
import { Banner } from "@/components/ui/banner";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/empty-state";
import { Skeleton } from "@/components/ui/skeleton";
import { Textarea } from "@/components/ui/textarea";
import { useApiErrorHandler } from "@/hooks/use-api-error";
import {
  useCompleteConversationMutation,
  useConversationQuery,
  useInlineFeedbackMutation,
  useSendMessageMutation
} from "@/hooks/use-conversations";
import { useToast } from "@/providers/ToastProvider";
import { formatDateTime } from "@/lib/utils";
import { useState } from "react";
import type { MessageFeedback } from "@/types/api";
import { ApiError } from "@/api/client";

export function ConversationPage() {
  const { conversationId = "" } = useParams();
  const navigate = useNavigate();
  const handleApiError = useApiErrorHandler();
  const { pushToast } = useToast();
  const conversationQuery = useConversationQuery(conversationId);
  const sendMessageMutation = useSendMessageMutation(conversationId);
  const feedbackMutation = useInlineFeedbackMutation(conversationId);
  const completeMutation = useCompleteConversationMutation(conversationId);
  const [draft, setDraft] = useState("");
  const [inlineFeedback, setInlineFeedback] = useState<Record<string, MessageFeedback & { feedback_summary?: string }>>({});
  const [openFeedbackId, setOpenFeedbackId] = useState<string | null>(null);

  const conversation = conversationQuery.data;
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const isCompleted = conversation?.status === "completed";

  const learnerMessages = useMemo(
    () => (conversation?.messages ?? []).filter((message) => message.sender === "user"),
    [conversation?.messages]
  );

  async function handleSend() {
    if (!draft.trim() || !conversation || isCompleted) return;

    const currentDraft = draft.trim();
    setDraft("");

    try {
      await sendMessageMutation.mutateAsync(currentDraft);
      pushToast({
        title: "Message sent",
        description: "The AI has responded to your latest turn."
      });
      queueMicrotask(() => messagesEndRef.current?.scrollIntoView({ behavior: "smooth" }));
    } catch (error) {
      if (error instanceof ApiError && error.status === 502 && error.data?.user_message) {
        pushToast({
          tone: "error",
          title: "AI reply failed",
          description: "Your message was saved, but the assistant could not answer. Reload or try again."
        });
        conversationQuery.refetch();
        return;
      }
      setDraft(currentDraft);
      handleApiError(error, "Could not send your message.");
    }
  }

  async function handleInlineFeedback(messageId: string) {
    if (inlineFeedback[messageId]) {
      setOpenFeedbackId((current) => (current === messageId ? null : messageId));
      return;
    }

    try {
      const response = await feedbackMutation.mutateAsync(messageId);
      setInlineFeedback((current) => ({
        ...current,
        [messageId]: {
          ...response.message_feedback,
          feedback_summary: response.feedback_summary
        }
      }));
      setOpenFeedbackId(messageId);
    } catch (error) {
      handleApiError(error, "Could not generate inline feedback.");
    }
  }

  async function handleComplete() {
    try {
      const result = await completeMutation.mutateAsync();
      if (result.final_feedback_error) {
        pushToast({
          tone: "error",
          title: "Used fallback final feedback",
          description: result.final_feedback_error
        });
      } else {
        pushToast({
          title: "Conversation completed",
          description: "Your final feedback and learner insights are ready."
        });
      }
      conversationQuery.refetch();
    } catch (error) {
      handleApiError(error, "Could not complete the conversation.");
    }
  }

  if (conversationQuery.isLoading) {
    return (
      <div className="grid gap-6 xl:grid-cols-[1.4fr_0.8fr]">
        <Skeleton className="h-[680px] w-full rounded-[28px]" />
        <div className="space-y-4">
          <Skeleton className="h-56 w-full rounded-[28px]" />
          <Skeleton className="h-80 w-full rounded-[28px]" />
        </div>
      </div>
    );
  }

  if (conversationQuery.isError || !conversation) {
    return <EmptyState title="Conversation unavailable" description="This conversation could not be loaded." actionLabel="Back to history" onAction={() => navigate("/app/history")} />;
  }

  return (
    <div className="grid gap-6 xl:grid-cols-[1.4fr_0.8fr]">
      <section className="space-y-4">
        <div className="sticky top-24 z-20 glass-panel p-5">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
            <div className="space-y-2">
              <Button variant="ghost" size="sm" onClick={() => navigate("/app/history")}>
                <ArrowLeft className="h-4 w-4" />
                Back
              </Button>
              <div className="flex flex-wrap items-center gap-3">
                <h1 className="text-2xl font-semibold text-slate-950">{conversation.scenario_name}</h1>
                <StatusBadge status={conversation.status} />
              </div>
              <p className="text-sm leading-7 text-slate-600">
                You are <span className="font-medium text-slate-900">{conversation.user_role_name}</span>. AI is{" "}
                <span className="font-medium text-slate-900">{conversation.ai_role_name ?? "the other role"}</span>.
              </p>
            </div>

            <div className="rounded-[24px] border border-slate-200 bg-white px-5 py-4 text-right shadow-sm">
              <p className="text-xs uppercase tracking-[0.2em] text-slate-400">Pacing</p>
              <p className="mt-2 text-lg font-semibold text-slate-950">{conversation.user_message_count} learner messages</p>
              <p className="text-sm text-slate-500">The AI will try to wrap up naturally once the scene feels complete.</p>
            </div>
          </div>
        </div>

        {conversation.opening_message_error ? (
          <Banner tone="warning" title="Opening message could not be generated automatically" description={conversation.opening_message_error} />
        ) : null}
        {sendMessageMutation.isError && !(sendMessageMutation.error instanceof ApiError && sendMessageMutation.error.status === 502) ? (
          <Banner
            tone="danger"
            title="Message could not be sent"
            description={sendMessageMutation.error instanceof Error ? sendMessageMutation.error.message : "Try again."}
          />
        ) : null}

        <Card className="overflow-hidden">
          <CardContent className="space-y-4 p-4 sm:p-6">
            <div className="max-h-[68vh] space-y-3 overflow-y-auto pr-1">
              {(conversation.messages ?? []).map((message) => (
                <div key={message.id}>
                  <ChatBubble
                    message={message}
                    aiRoleName={conversation.ai_role_name}
                    feedbackVisible={openFeedbackId === message.id}
                    hasFeedback={Boolean(inlineFeedback[message.id])}
                    onToggleFeedback={message.sender === "user" ? () => handleInlineFeedback(message.id) : undefined}
                    canRequestFeedback={!isCompleted}
                    requestingFeedback={feedbackMutation.isPending && feedbackMutation.variables === message.id}
                  />
                  {openFeedbackId === message.id && inlineFeedback[message.id] ? <FeedbackCard feedback={inlineFeedback[message.id]} /> : null}
                </div>
              ))}

              {sendMessageMutation.isPending ? (
                <div className="flex items-center gap-3 rounded-[24px] border border-white/70 bg-white/80 px-4 py-3 text-sm text-slate-600">
                  <LoaderCircle className="h-4 w-4 animate-spin" />
                  Waiting for the AI to answer...
                </div>
              ) : null}

              <div ref={messagesEndRef} />
            </div>

            <div className="rounded-[28px] border border-slate-200 bg-slate-50/60 p-3">
              <Textarea
                placeholder={
                  isCompleted
                    ? "This conversation is complete and read-only."
                    : "Write your next reply in German..."
                }
                value={draft}
                onChange={(event) => setDraft(event.target.value)}
                disabled={isCompleted || sendMessageMutation.isPending}
                className="border-0 bg-transparent px-3 py-2 shadow-none focus:ring-0"
              />
              <div className="mt-3 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <p className="text-sm text-slate-500">
                  Completed conversations are read-only. Inline feedback is available on learner messages.
                </p>
                <div className="flex items-center gap-2">
                  <Button
                    variant="secondary"
                    onClick={handleComplete}
                    disabled={isCompleted || completeMutation.isPending || learnerMessages.length === 0}
                  >
                    {completeMutation.isPending ? "Completing..." : "Complete conversation"}
                  </Button>
                  <Button onClick={handleSend} disabled={!draft.trim() || isCompleted || sendMessageMutation.isPending}>
                    Send
                  </Button>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      <aside className="space-y-4">
        <Card>
          <CardHeader>
            <CardTitle>Conversation notes</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4 text-sm leading-7 text-slate-600">
            <div>
              <p className="font-medium text-slate-900">Scenario</p>
              <p>{conversation.scenario_description}</p>
            </div>
            <div>
              <p className="font-medium text-slate-900">Started</p>
              <p>{formatDateTime(conversation.started_at)}</p>
            </div>
            <div>
              <p className="font-medium text-slate-900">Role setup</p>
              <p>
                You are {conversation.user_role_name}. AI is {conversation.ai_role_name ?? "the other role"}.
              </p>
            </div>
          </CardContent>
        </Card>

        {conversation.feedback ? (
          <Card className="border-cyan-100 bg-cyan-50/70">
            <CardHeader>
              <div className="flex items-center gap-2 text-accent">
                <Sparkles className="h-4 w-4" />
                <span className="text-sm font-semibold uppercase tracking-[0.2em]">Final review</span>
              </div>
              <CardTitle>{conversation.feedback.overall_feedback ?? "Final feedback available"}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {completeMutation.data?.profile_update_error ? (
                <Banner tone="warning" title="Profile update warning" description={completeMutation.data.profile_update_error} />
              ) : null}
              {completeMutation.data?.final_feedback_error ? (
                <Banner tone="warning" title="Final feedback warning" description={completeMutation.data.final_feedback_error} />
              ) : null}
              <div className="space-y-3">
                {conversation.feedback.message_feedback.map((item) => (
                  <div key={item.id} className="rounded-2xl bg-white/80 p-3 text-sm text-slate-700">
                    <p className="font-medium text-slate-900">Original</p>
                    <p>{item.original_text}</p>
                    <p className="mt-3 font-medium text-slate-900">Corrected</p>
                    <p>{item.corrected_text}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        ) : (
          <Card className="border-dashed">
            <CardContent className="flex flex-col items-center gap-3 p-8 text-center">
              <MessageSquareOff className="h-10 w-10 text-slate-300" />
              <p className="font-medium text-slate-900">No final feedback yet</p>
              <p className="text-sm text-slate-500">
                Finish the conversation when you are ready to get a complete lesson-style review.
              </p>
            </CardContent>
          </Card>
        )}
      </aside>
    </div>
  );
}
