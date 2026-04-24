import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";

import { api, ApiError } from "@/api/client";
import type { User } from "@/types/api";

type AuthContextValue = {
  token: string | null;
  user: User | null;
  isAuthenticated: boolean;
  bootstrapping: boolean;
  login: (payload: { email: string; password: string }) => Promise<User>;
  register: (payload: {
    email: string;
    password: string;
    plan: string;
    german_level: string;
    native_language: string;
  }) => Promise<User>;
  logout: () => void;
};

const STORAGE_KEY = "deutsch-flow.auth";
const AuthContext = createContext<AuthContextValue | null>(null);

function readSession() {
  try {
    const value = window.localStorage.getItem(STORAGE_KEY);
    if (!value) return { token: null as string | null, user: null as User | null };
    return JSON.parse(value) as { token: string | null; user: User | null };
  } catch {
    return { token: null as string | null, user: null as User | null };
  }
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const initial = readSession();
  const [token, setToken] = useState<string | null>(initial.token);
  const [user, setUser] = useState<User | null>(initial.user);
  const [bootstrapping, setBootstrapping] = useState(Boolean(initial.token));

  useEffect(() => {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify({ token, user }));
  }, [token, user]);

  useEffect(() => {
    let ignore = false;
    const controller = new AbortController();

    async function bootstrap() {
      if (!token) {
        setBootstrapping(false);
        return;
      }

      try {
        const currentUser = await api.me(token, controller.signal);
        if (!ignore) setUser(currentUser);
      } catch (error) {
        if (!ignore && error instanceof ApiError && error.status === 401) {
          setToken(null);
          setUser(null);
        }
      } finally {
        if (!ignore) setBootstrapping(false);
      }
    }

    bootstrap();
    return () => {
      ignore = true;
      controller.abort();
    };
  }, [token]);

  const login = useCallback(async (payload: { email: string; password: string }) => {
    const response = await api.login(payload);
    setToken(response.access_token);
    setUser(response.user);
    return response.user;
  }, []);

  const register = useCallback(
    async (payload: {
      email: string;
      password: string;
      plan: string;
      german_level: string;
      native_language: string;
    }) => {
      const response = await api.register(payload);
      setToken(response.access_token);
      setUser(response.user);
      return response.user;
    },
    []
  );

  const logout = useCallback(() => {
    setToken(null);
    setUser(null);
    window.localStorage.removeItem(STORAGE_KEY);
  }, []);

  const value = useMemo<AuthContextValue>(
    () => ({
      token,
      user,
      isAuthenticated: Boolean(token),
      bootstrapping,
      login,
      register,
      logout
    }),
    [token, user, bootstrapping, login, register, logout]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider.");
  }
  return context;
}
