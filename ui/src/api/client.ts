import type {
  ApiErrorPayload,
  AuthResponse,
  CompleteConversationResponse,
  ConversationDetail,
  ConversationListItem,
  ConversationTurnResponse,
  FeedbackSession,
  InlineFeedbackResponse,
  Scenario,
  ScenarioRole,
  User
} from "@/types/api";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";

export class ApiError extends Error {
  status: number;
  data: ApiErrorPayload | null;

  constructor(message: string, status: number, data: ApiErrorPayload | null = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.data = data;
  }
}

type RequestOptions = {
  method?: "GET" | "POST";
  body?: unknown;
  token?: string | null;
  signal?: AbortSignal;
};

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: options.method ?? "GET",
    headers: {
      ...(options.body ? { "Content-Type": "application/json" } : {}),
      ...(options.token ? { Authorization: `Bearer ${options.token}` } : {})
    },
    body: options.body ? JSON.stringify(options.body) : undefined,
    signal: options.signal
  });

  const rawText = await response.text();
  const data = rawText ? safeParse(rawText) : null;

  if (!response.ok) {
    const message = typeof data?.error === "string" ? data.error : `Request failed with HTTP ${response.status}.`;
    throw new ApiError(message, response.status, data as ApiErrorPayload | null);
  }

  return data as T;
}

function safeParse(value: string) {
  try {
    return JSON.parse(value);
  } catch {
    return { error: value };
  }
}

export const api = {
  health: () => request<{ status: string }>("/api/health"),
  login: (payload: { email: string; password: string }) =>
    request<AuthResponse>("/api/auth/login", { method: "POST", body: payload }),
  register: (payload: {
    email: string;
    password: string;
    plan: string;
    german_level: string;
    native_language: string;
  }) => request<AuthResponse>("/api/auth/register", { method: "POST", body: payload }),
  me: (token: string, signal?: AbortSignal) => request<User>("/api/auth/me", { token, signal }),
  scenarios: () => request<Scenario[]>("/api/scenarios"),
  scenario: (scenarioId: string) => request<Scenario>(`/api/scenarios/${scenarioId}`),
  scenarioRoles: (scenarioId: string) => request<ScenarioRole[]>(`/api/scenarios/${scenarioId}/roles`),
  conversations: (token: string) => request<ConversationListItem[]>("/api/conversations", { token }),
  createConversation: (
    token: string,
    payload: { scenario_id: string; scenario_role_id: string; generate_opening_message?: boolean }
  ) => request<ConversationDetail>("/api/conversations", { method: "POST", token, body: payload }),
  conversation: (token: string, conversationId: string, signal?: AbortSignal) =>
    request<ConversationDetail>(`/api/conversations/${conversationId}`, { token, signal }),
  sendMessage: (token: string, conversationId: string, content: string) =>
    request<ConversationTurnResponse>(`/api/conversations/${conversationId}/messages`, {
      method: "POST",
      token,
      body: { content }
    }),
  messageFeedback: (token: string, conversationId: string, messageId: string) =>
    request<InlineFeedbackResponse>(`/api/conversations/${conversationId}/messages/${messageId}/feedback`, {
      method: "POST",
      token
    }),
  conversationFeedback: (token: string, conversationId: string) =>
    request<FeedbackSession>(`/api/conversations/${conversationId}/feedback`, { token }),
  completeConversation: (token: string, conversationId: string) =>
    request<CompleteConversationResponse>(`/api/conversations/${conversationId}/complete`, {
      method: "POST",
      token
    })
};
