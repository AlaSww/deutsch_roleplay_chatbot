import { Badge } from "@/components/ui/badge";
import type { ConversationStatus } from "@/types/api";

export function StatusBadge({ status }: { status: ConversationStatus }) {
  return <Badge tone={status === "active" ? "success" : "default"}>{status === "active" ? "Active" : "Completed"}</Badge>;
}
