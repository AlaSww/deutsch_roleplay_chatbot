import { MessageSquareQuote } from "lucide-react";

import { Button } from "@/components/ui/button";
import { cn, formatDateTime } from "@/lib/utils";
import type { Message } from "@/types/api";

export function ChatBubble({
  message,
  aiRoleName,
  feedbackVisible,
  onToggleFeedback,
  hasFeedback,
  canRequestFeedback,
  requestingFeedback
}: {
  message: Message;
  aiRoleName: string | null;
  feedbackVisible?: boolean;
  onToggleFeedback?: () => void;
  hasFeedback?: boolean;
  canRequestFeedback?: boolean;
  requestingFeedback?: boolean;
}) {
  const isUser = message.sender === "user";

  return (
    <div className={cn("flex w-full animate-fade-up", isUser ? "justify-end" : "justify-start")}>
      <div
        className={cn(
          "max-w-[88%] rounded-[22px] px-4 py-3 sm:max-w-[78%]",
          isUser
            ? "bg-slate-950 text-white"
            : "border border-slate-200 bg-white text-slate-900"
        )}
      >
        <div className="mb-2 flex items-center justify-between gap-3">
          <p className={cn("text-xs font-semibold uppercase tracking-[0.18em]", isUser ? "text-white/70" : "text-slate-500")}>
            {isUser ? "You" : aiRoleName ?? "AI role"}
          </p>
          <p className={cn("text-xs", isUser ? "text-white/60" : "text-slate-400")}>{formatDateTime(message.created_at)}</p>
        </div>
        <p className="whitespace-pre-wrap text-sm leading-7">{message.content}</p>

        {isUser && onToggleFeedback ? (
          <div className="mt-3 flex justify-end">
            <Button
              size="sm"
              variant={feedbackVisible ? "secondary" : "ghost"}
              onClick={onToggleFeedback}
              disabled={requestingFeedback || !canRequestFeedback}
              className={cn("h-8 rounded-full px-3 text-xs", isUser && !feedbackVisible ? "text-white/80 hover:bg-white/10 hover:text-white" : "")}
            >
              <MessageSquareQuote className="h-4 w-4" />
              {requestingFeedback ? "Checking..." : hasFeedback ? "View feedback" : "Check this message"}
            </Button>
          </div>
        ) : null}
      </div>
    </div>
  );
}
