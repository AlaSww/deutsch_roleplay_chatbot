import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "@/providers/AuthProvider";

export function useAuthGuard() {
  const auth = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!auth.bootstrapping && !auth.isAuthenticated) {
      navigate("/login", { replace: true });
    }
  }, [auth.bootstrapping, auth.isAuthenticated, navigate]);

  return auth;
}
