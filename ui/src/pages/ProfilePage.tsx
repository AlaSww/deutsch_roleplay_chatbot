import { Award, Brain, Languages, NotebookPen, TrendingUp } from "lucide-react";

import { ProfileInsightCard } from "@/components/profile/ProfileInsightCard";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuth } from "@/providers/AuthProvider";

export function ProfilePage() {
  const { user } = useAuth();
  const profile = user?.user_profile;

  return (
    <div className="space-y-6">
      <section className="glass-panel p-8">
        <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.2em] text-accent">Learner progress</p>
            <h1 className="mt-3 font-display text-5xl text-ink">A clear picture of where your German is growing next.</h1>
            <p className="mt-4 max-w-3xl text-base leading-8 text-slate-600">
              Your profile evolves after completed conversations. It captures recurring mistakes, grammar areas to
              focus on, vocabulary gaps, and strengths worth reinforcing.
            </p>
          </div>
          <Card className="min-w-[280px]">
            <CardHeader>
              <CardTitle className="text-lg">Profile snapshot</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-sm text-slate-600">
              <div className="flex items-center justify-between">
                <span>German level</span>
                <Badge tone="accent">{user?.german_level ?? "A1"}</Badge>
              </div>
              <div className="flex items-center justify-between">
                <span>Native language</span>
                <span className="font-medium text-slate-900">{user?.native_language ?? "English"}</span>
              </div>
              <div className="flex items-center justify-between">
                <span>Plan</span>
                <Badge tone={user?.plan === "premium" ? "premium" : "default"}>{user?.plan ?? "free"}</Badge>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
        <ProfileInsightCard
          title="Strengths"
          icon={<Award className="h-5 w-5" />}
          items={profile?.strengths ?? []}
          description="What you consistently do well and should keep using."
        />
        <ProfileInsightCard
          title="Common mistakes"
          icon={<TrendingUp className="h-5 w-5" />}
          items={profile?.common_mistakes ?? []}
          description="Recurring issues worth addressing in future sessions."
        />
        <ProfileInsightCard
          title="Grammar focus"
          icon={<Brain className="h-5 w-5" />}
          items={profile?.grammar_focus_areas ?? []}
          description="The next grammar topics that give you the biggest payoff."
        />
        <ProfileInsightCard
          title="Vocabulary gaps"
          icon={<Languages className="h-5 w-5" />}
          items={profile?.vocabulary_gaps ?? []}
          description="Word groups and domains that need more repetition."
        />
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <NotebookPen className="h-5 w-5 text-accent" />
            Latest feedback summary
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm leading-8 text-slate-700">
            {profile?.last_feedback_summary ??
              "Complete a conversation to generate your first learner summary and keep this profile evolving over time."}
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
