import { BookOpenText, LayoutDashboard, LogOut, Menu, MessagesSquare, Sparkles } from "lucide-react";
import { NavLink, useLocation } from "react-router-dom";
import { useState } from "react";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { useAuth } from "@/providers/AuthProvider";

const navItems = [
  { to: "/app/scenarios", label: "Scenarios", icon: Sparkles },
  { to: "/app/history", label: "History", icon: MessagesSquare },
  { to: "/app/profile", label: "Progress", icon: LayoutDashboard }
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const { pathname } = useLocation();
  const { user, logout, isAuthenticated } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-40 border-b border-slate-200/80 bg-white/95">
        <div className="page-shell flex h-20 items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            {isAuthenticated ? (
              <button
                className="inline-flex rounded-full p-2 text-slate-700 lg:hidden"
                onClick={() => setMobileOpen((value) => !value)}
                type="button"
              >
                <Menu className="h-5 w-5" />
              </button>
            ) : null}
            <NavLink to="/" className="flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-slate-950 text-white shadow-soft">
                <BookOpenText className="h-5 w-5" />
              </div>
              <div>
                <p className="font-semibold text-slate-950">Deutsch Flow</p>
                <p className="text-xs text-slate-500">AI roleplay for practical German</p>
              </div>
            </NavLink>
          </div>

          {isAuthenticated ? (
            <div className="hidden items-center gap-3 lg:flex">
              {navItems.map((item) => (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={({ isActive }) =>
                    cn(
                      "rounded-full px-4 py-2 text-sm font-medium transition",
                      isActive ? "bg-slate-950 text-white" : "text-slate-600 hover:bg-white hover:text-slate-900"
                    )
                  }
                >
                  {item.label}
                </NavLink>
              ))}
            </div>
          ) : null}

          <div className="flex items-center gap-3">
            {isAuthenticated && user ? (
              <>
                <div className="hidden text-right sm:block">
                  <p className="text-sm font-medium text-slate-950">{user.email}</p>
                  <p className="text-xs text-slate-500">
                    {user.plan} plan · {user.german_level ?? "A1"}
                  </p>
                </div>
                <Button variant="secondary" size="sm" onClick={logout}>
                  <LogOut className="h-4 w-4" />
                  Logout
                </Button>
              </>
            ) : (
              <div className="flex items-center gap-2">
                <NavLink to="/login">
                  <Button variant="ghost" size="sm">
                    Login
                  </Button>
                </NavLink>
                <NavLink to="/register">
                  <Button size="sm">Start free</Button>
                </NavLink>
              </div>
            )}
          </div>
        </div>

        {isAuthenticated ? (
          <div className={cn("border-t border-slate-200/80 lg:hidden", mobileOpen ? "block" : "hidden")}>
            <div className="page-shell flex flex-col gap-2 py-3">
              {navItems.map((item) => {
                const Icon = item.icon;
                const active = pathname.startsWith(item.to);
                return (
                  <NavLink
                    key={item.to}
                    className={cn(
                      "flex items-center gap-3 rounded-2xl px-4 py-3 text-sm font-medium",
                      active ? "bg-slate-950 text-white" : "bg-slate-50 text-slate-700"
                    )}
                    onClick={() => setMobileOpen(false)}
                    to={item.to}
                  >
                    <Icon className="h-4 w-4" />
                    {item.label}
                  </NavLink>
                );
              })}
            </div>
          </div>
        ) : null}
      </header>

      <main className="page-shell py-6 sm:py-8">{children}</main>
    </div>
  );
}
