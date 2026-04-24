import { useMutation } from "@tanstack/react-query";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { AuthForm } from "@/components/app/AuthForm";
import { useAuth } from "@/providers/AuthProvider";

export function RegisterPage() {
  const navigate = useNavigate();
  const { register } = useAuth();
  const [values, setValues] = useState({
    email: "",
    password: "",
    german_level: "A2",
    native_language: "English",
    plan: "free"
  });
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});

  const mutation = useMutation({
    mutationFn: register,
    onSuccess: () => navigate("/app/scenarios", { replace: true })
  });

  const generalError = mutation.error instanceof Error ? mutation.error.message : undefined;

  function handleSubmit() {
    const nextErrors: Record<string, string> = {};
    if (!values.email.trim()) nextErrors.email = "Email is required.";
    if (values.password.trim().length < 8) nextErrors.password = "Password must be at least 8 characters.";
    if (!values.native_language.trim()) nextErrors.native_language = "Native language is required.";
    setFieldErrors(nextErrors);
    if (Object.keys(nextErrors).length) return;
    mutation.mutate(values);
  }

  return (
    <div className="grid gap-8 lg:grid-cols-[0.9fr_1.1fr]">
      <div className="glass-panel p-8">
        <p className="text-sm uppercase tracking-[0.2em] text-accent">Create your learner profile</p>
        <h1 className="mt-3 font-display text-5xl text-ink">Build a practice space that adapts to you.</h1>
        <p className="mt-4 max-w-md text-base leading-8 text-slate-600">
          Your level, native language, strengths, and gaps influence how the AI responds and what feedback it
          prioritizes after each roleplay.
        </p>
      </div>

      <AuthForm
        mode="register"
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
