import { Eye, EyeOff } from "lucide-react";
import { useState } from "react";
import { Link } from "react-router-dom";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

type FieldErrors = Record<string, string>;

export function AuthForm({
  mode,
  loading,
  error,
  values,
  fieldErrors,
  onChange,
  onSubmit
}: {
  mode: "login" | "register";
  loading: boolean;
  error?: string;
  values: Record<string, string>;
  fieldErrors: FieldErrors;
  onChange: (field: string, value: string) => void;
  onSubmit: () => void;
}) {
  const [showPassword, setShowPassword] = useState(false);
  const isRegister = mode === "register";

  return (
    <Card className="mx-auto w-full max-w-xl">
      <CardHeader className="space-y-3">
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-accent">{isRegister ? "Create account" : "Welcome back"}</p>
        <CardTitle className="text-3xl">{isRegister ? "Start your German speaking routine" : "Log in to continue practicing"}</CardTitle>
        <CardDescription>
          {isRegister
            ? "Set your learner profile now. The AI will use it to adjust difficulty, prompts, and feedback."
            : "Use your account to jump back into scenarios, chat history, and learner progress."}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-5">
        <div className="grid gap-4">
          <Field
            label="Email"
            error={fieldErrors.email}
            input={<Input type="email" placeholder="you@example.com" value={values.email} onChange={(e) => onChange("email", e.target.value)} />}
          />

          <Field
            label="Password"
            error={fieldErrors.password}
            input={
              <div className="relative">
                <Input
                  type={showPassword ? "text" : "password"}
                  placeholder="At least 8 characters"
                  value={values.password}
                  onChange={(e) => onChange("password", e.target.value)}
                  className="pr-12"
                />
                <button
                  type="button"
                  className="absolute right-3 top-3 text-slate-500"
                  onClick={() => setShowPassword((value) => !value)}
                >
                  {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                </button>
              </div>
            }
          />

          {isRegister ? (
            <>
              <div className="grid gap-4 sm:grid-cols-2">
                <Field
                  label="German level"
                  error={fieldErrors.german_level}
                  input={
                    <select
                      className="h-12 w-full rounded-2xl border border-slate-200 bg-white px-4 text-sm outline-none focus:border-accent focus:ring-4 focus:ring-accent/10"
                      value={values.german_level}
                      onChange={(e) => onChange("german_level", e.target.value)}
                    >
                      {["A1", "A2", "B1", "B2", "C1", "C2"].map((level) => (
                        <option key={level}>{level}</option>
                      ))}
                    </select>
                  }
                />
                <Field
                  label="Plan"
                  error={fieldErrors.plan}
                  input={
                    <select
                      className="h-12 w-full rounded-2xl border border-slate-200 bg-white px-4 text-sm outline-none focus:border-accent focus:ring-4 focus:ring-accent/10"
                      value={values.plan}
                      onChange={(e) => onChange("plan", e.target.value)}
                    >
                      <option value="free">Free</option>
                      <option value="premium">Premium</option>
                    </select>
                  }
                />
              </div>
              <Field
                label="Native language"
                error={fieldErrors.native_language}
                input={<Input value={values.native_language} onChange={(e) => onChange("native_language", e.target.value)} />}
              />
            </>
          ) : null}
        </div>

        {error ? <p className="rounded-2xl bg-rose-50 px-4 py-3 text-sm text-rose-700">{error}</p> : null}

        <Button className="w-full" onClick={onSubmit} disabled={loading}>
          {loading ? "Working..." : isRegister ? "Create account" : "Log in"}
        </Button>

        <p className="text-center text-sm text-slate-500">
          {isRegister ? "Already have an account?" : "Need an account?"}{" "}
          <Link className="font-medium text-slate-950 underline-offset-4 hover:underline" to={isRegister ? "/login" : "/register"}>
            {isRegister ? "Log in" : "Create one"}
          </Link>
        </p>
      </CardContent>
    </Card>
  );
}

function Field({ label, input, error }: { label: string; input: React.ReactNode; error?: string }) {
  return (
    <label className="grid gap-2 text-sm font-medium text-slate-700">
      <span>{label}</span>
      {input}
      {error ? <span className="text-xs text-rose-600">{error}</span> : null}
    </label>
  );
}
