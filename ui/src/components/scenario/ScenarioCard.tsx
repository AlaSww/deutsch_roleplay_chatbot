import { Crown, Lock, Sparkles } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { Scenario } from "@/types/api";

export function ScenarioCard({
  scenario,
  locked,
  onOpen
}: {
  scenario: Scenario;
  locked: boolean;
  onOpen: () => void;
}) {
  return (
    <Card className="group h-full overflow-hidden transition duration-300 hover:-translate-y-1 hover:shadow-soft">
      <CardHeader className="space-y-4">
        <div className="flex items-center justify-between gap-2">
          <Badge tone={scenario.is_premium ? "premium" : "accent"}>
            {scenario.is_premium ? (
              <>
                <Crown className="mr-1 h-3 w-3" /> Premium
              </>
            ) : (
              <>
                <Sparkles className="mr-1 h-3 w-3" /> Free
              </>
            )}
          </Badge>
          <Badge tone="default">{scenario.roles.length} roles</Badge>
        </div>
        <div>
          <CardTitle>{scenario.name}</CardTitle>
          <p className="mt-2 text-sm leading-6 text-slate-600">{scenario.description}</p>
        </div>
      </CardHeader>
      <CardContent className="space-y-5">
        <div className="flex flex-wrap gap-2">
          {scenario.roles.map((role) => (
            <Badge key={role.id} tone="default" className="bg-slate-100">
              {role.role_name}
            </Badge>
          ))}
        </div>
        <Button className="w-full" onClick={onOpen} variant={locked ? "secondary" : "primary"}>
          {locked ? (
            <>
              <Lock className="h-4 w-4" />
              Premium style lock
            </>
          ) : (
            "Choose role"
          )}
        </Button>
      </CardContent>
    </Card>
  );
}
