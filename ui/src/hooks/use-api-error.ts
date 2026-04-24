import { useNavigate } from "react-router-dom";

import { ApiError } from "@/api/client";
import { useAuth } from "@/providers/AuthProvider";
import { useToast } from "@/providers/ToastProvider";

export function useApiErrorHandler() {
  const { logout } = useAuth();
  const { pushToast } = useToast();
  const navigate = useNavigate();

  return (error: unknown, fallbackMessage = "Something went wrong.") => {
    if (error instanceof ApiError && error.status === 401) {
      logout();
      navigate("/login", { replace: true });
      return;
    }

    const message = error instanceof ApiError ? error.message : fallbackMessage;
    pushToast({
      tone: "error",
      title: "Request failed",
      description: message
    });
  };
}
