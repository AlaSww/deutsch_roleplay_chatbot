import { ArrowRight, BadgeCheck, Languages, MessageCircleMore, Sparkles } from "lucide-react";
import { Link } from "react-router-dom";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

const scenarios = ["Cafe Visit", "Apartment Viewing", "Job Interview", "Doctor Appointment", "Train Station Help"];

export function LandingPage() {
  return (
    <div className="space-y-8">
      <section className="grid gap-6 lg:grid-cols-[1.25fr_0.85fr]">
        <div className="glass-panel overflow-hidden p-8 sm:p-10">
          <Badge tone="accent" className="mb-5">
            Premium AI speaking practice
          </Badge>
          <h1 className="display-title max-w-3xl">
            Learn German through <span className="text-accent">real conversations</span>, not isolated drills.
          </h1>
          <p className="mt-5 max-w-2xl text-lg leading-8 text-slate-600">
            Pick a scenario, choose your role, chat naturally with the AI, request corrections exactly when you
            need them, and finish each session with a thoughtful review of how your German is evolving.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link to="/register">
              <Button size="lg">
                Start free
                <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
            <Link to="/login">
              <Button variant="secondary" size="lg">
                Log in
              </Button>
            </Link>
          </div>
          <div className="mt-10 grid gap-4 sm:grid-cols-3">
            <Feature label="Role-first learning" description="Speak from a perspective and keep the scene moving." icon={<Languages className="h-5 w-5" />} />
            <Feature label="Inline corrections" description="Check one message without breaking your whole flow." icon={<MessageCircleMore className="h-5 w-5" />} />
            <Feature label="Progress memory" description="The app tracks your strengths, gaps, and patterns." icon={<BadgeCheck className="h-5 w-5" />} />
          </div>
        </div>

        <div className="grid gap-4">
          <Card className="animate-float p-6">
            <div className="rounded-[24px] bg-slate-950 p-5 text-white">
              <p className="text-xs uppercase tracking-[0.2em] text-white/60">How it works</p>
              <ul className="mt-4 space-y-3 text-sm leading-7 text-white/80">
                <li>1. Browse scenario cards.</li>
                <li>2. Choose the role you want to practice.</li>
                <li>3. Chat naturally in German.</li>
                <li>4. Ask for feedback on any learner message.</li>
                <li>5. Complete the conversation for a lesson-style review.</li>
              </ul>
            </div>
          </Card>
          <Card className="p-6">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Popular scenarios</p>
            <div className="mt-4 flex flex-wrap gap-2">
              {scenarios.map((scenario) => (
                <Badge key={scenario} tone="default" className="bg-slate-100 px-4 py-2 text-sm">
                  <Sparkles className="mr-2 h-4 w-4 text-accent" />
                  {scenario}
                </Badge>
              ))}
            </div>
          </Card>
        </div>
      </section>
    </div>
  );
}

function Feature({ label, description, icon }: { label: string; description: string; icon: React.ReactNode }) {
  return (
    <div className="rounded-3xl bg-white/70 p-4 shadow-sm">
      <div className="mb-3 inline-flex rounded-2xl bg-slate-100 p-3 text-slate-700">{icon}</div>
      <p className="font-medium text-slate-950">{label}</p>
      <p className="mt-2 text-sm leading-6 text-slate-600">{description}</p>
    </div>
  );
}
