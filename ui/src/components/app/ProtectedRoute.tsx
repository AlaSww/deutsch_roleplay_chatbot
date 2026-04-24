import { Navigate, useLocation } from "react-router-dom";

import { EmptyState } from "@/components/ui/empty-state";
import { useAuth } from "@/providers/AuthProvider";

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const auth = useAuth();
  const location = useLocation();

  if (auth.bootstrapping) {
    return (
      <div className="py-20">
        <EmptyState title="Restoring your session" description="Checking your learner account and preparing your dashboard." />
      </div>
    );
  }

  if (!auth.isAuthenticated) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }

  return <>{children}</>;
}
