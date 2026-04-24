import type { ReactNode } from "react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export function ProfileInsightCard({
  title,
  icon,
  items,
  description
}: {
  title: string;
  icon: ReactNode;
  items: string[];
  description?: string;
}) {
  return (
    <Card className="h-full">
      <CardHeader className="space-y-3">
        <div className="flex items-center gap-3">
          <div className="rounded-2xl bg-slate-100 p-3 text-slate-700">{icon}</div>
          <CardTitle>{title}</CardTitle>
        </div>
        {description ? <p className="text-sm text-slate-600">{description}</p> : null}
      </CardHeader>
      <CardContent className="flex flex-wrap gap-2">
        {items.length ? (
          items.map((item) => (
            <Badge key={item} tone="default" className="bg-slate-100 text-slate-700">
              {item}
            </Badge>
          ))
        ) : (
          <p className="text-sm text-slate-500">Nothing recorded yet.</p>
        )}
      </CardContent>
    </Card>
  );
}
