import { useMutation } from "@tanstack/react-query";
import { useMemo, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import { AuthForm } from "@/components/app/AuthForm";
import { useAuth } from "@/providers/AuthProvider";

export function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();
  const [values, setValues] = useState({ email: "", password: "" });
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});

  const destination = (location.state as { from?: string } | null)?.from ?? "/app/scenarios";

  const mutation = useMutation({
    mutationFn: login,
    onSuccess: () => navigate(destination, { replace: true })
  });

  const generalError = mutation.error instanceof Error ? mutation.error.message : undefined;

  function handleSubmit() {
    const nextErrors: Record<string, string> = {};
    if (!values.email.trim()) nextErrors.email = "Email is required.";
    if (!values.password.trim()) nextErrors.password = "Password is required.";
    setFieldErrors(nextErrors);
    if (Object.keys(nextErrors).length) return;
    mutation.mutate(values);
  }

  return (
    <div className="grid gap-8 lg:grid-cols-[0.9fr_1.1fr]">
      <div className="glass-panel p-8">
        <p className="text-sm uppercase tracking-[0.2em] text-accent">Welcome back</p>
        <h1 className="mt-3 font-display text-5xl text-ink">Your next conversation is waiting.</h1>
        <p className="mt-4 max-w-md text-base leading-8 text-slate-600">
          Pick up where you left off, continue active roleplays, review completed sessions, and keep your German
          improving with focused feedback.
        </p>
      </div>

      <AuthForm
        mode="login"
        loading={mutation.isPending}
        error={generalError}
        values={values}
        fieldErrors={fieldErrors}
        onChange={(field, value) => setValues((current) => ({ ...current, [field]: value }))}
        onSubmit={handleSubmit}
      />
    </div>
  );
}
