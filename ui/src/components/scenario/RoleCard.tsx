import { ArrowRight, CheckCircle2, UserRound } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import type { ScenarioRole } from "@/types/api";

export function RoleCard({
  role,
  oppositeRoleName,
  selected,
  onSelect
}: {
  role: ScenarioRole;
  oppositeRoleName?: string | null;
  selected: boolean;
  onSelect: () => void;
}) {
  return (
    <button className="h-full text-left" onClick={onSelect} type="button">
      <Card
        className={cn(
          "h-full transition duration-200 hover:-translate-y-1 hover:shadow-soft",
          selected ? "ring-2 ring-accent/40" : "ring-0"
        )}
      >
        <CardHeader className="space-y-4">
          <div className="flex items-center justify-between">
            <Badge tone={selected ? "accent" : "default"}>{selected ? "Selected" : "Choose this role"}</Badge>
            {selected ? <CheckCircle2 className="h-5 w-5 text-accent" /> : <UserRound className="h-5 w-5 text-slate-400" />}
          </div>
          <CardTitle>{role.role_name}</CardTitle>
          <p className="text-sm leading-6 text-slate-600">{role.prompt_context}</p>
        </CardHeader>
        <CardContent className="flex items-center gap-2 text-sm text-slate-500">
          <ArrowRight className="h-4 w-4" />
          AI will play {oppositeRoleName ?? "the opposite role"}
        </CardContent>
      </Card>
    </button>
  );
}
