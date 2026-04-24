import { Lightbulb, SpellCheck2, WandSparkles } from "lucide-react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { InlineFeedbackResponse, MessageFeedback } from "@/types/api";

type CombinedFeedback = MessageFeedback & { feedback_summary?: string };

export function FeedbackCard({ feedback }: { feedback: CombinedFeedback }) {
  return (
    <Card className="ml-auto mt-3 w-full max-w-3xl border-slate-200 bg-slate-50/80">
      <CardHeader>
        <CardTitle className="text-lg">Helpful review</CardTitle>
        {feedback.feedback_summary ? <p className="text-sm text-slate-600">{feedback.feedback_summary}</p> : null}
      </CardHeader>
      <CardContent className="grid gap-4">
        <section className="rounded-3xl bg-white p-4">
          <div className="mb-2 flex items-center gap-2 text-sm font-medium text-slate-700">
            <SpellCheck2 className="h-4 w-4" />
            Corrected text
          </div>
          <p className="text-sm leading-7 text-slate-900">{feedback.corrected_text}</p>
        </section>

        <div className="grid gap-4 lg:grid-cols-2">
          <section className="rounded-3xl bg-white p-4">
            <div className="mb-2 flex items-center gap-2 text-sm font-medium text-slate-700">
              <WandSparkles className="h-4 w-4" />
              Mistakes
            </div>
            {feedback.mistakes.length ? (
              <ul className="space-y-3 text-sm text-slate-700">
                {feedback.mistakes.map((mistake, index) => (
                  <li key={`${mistake.span}-${index}`} className="rounded-2xl bg-slate-50 p-3">
                    <p className="font-medium text-slate-900">{mistake.span}</p>
                    <p>{mistake.issue}</p>
                    <p className="mt-1 text-xs uppercase tracking-[0.2em] text-slate-400">{mistake.category}</p>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-slate-600">No major mistakes detected.</p>
            )}
          </section>

          <section className="rounded-3xl bg-white p-4">
            <div className="mb-2 flex items-center gap-2 text-sm font-medium text-slate-700">
              <Lightbulb className="h-4 w-4" />
              Better alternatives
            </div>
            {feedback.better_alternatives.length ? (
              <ul className="space-y-3 text-sm text-slate-700">
                {feedback.better_alternatives.map((alternative) => (
                  <li key={alternative} className="rounded-2xl bg-slate-50 p-3">
                    {alternative}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-slate-600">No extra alternatives returned for this message.</p>
            )}
          </section>
        </div>

        <section className="rounded-3xl bg-white p-4">
          <div className="mb-2 text-sm font-medium text-slate-700">Explanations</div>
          {feedback.explanations.length ? (
            <ul className="space-y-2 text-sm leading-7 text-slate-700">
              {feedback.explanations.map((item) => (
                <li key={item} className="rounded-2xl bg-slate-50 px-3 py-2">
                  {item}
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-slate-600">No explanation returned.</p>
          )}
        </section>
      </CardContent>
    </Card>
  );
}
