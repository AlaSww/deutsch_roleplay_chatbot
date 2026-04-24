export type Plan = "free" | "premium";
export type ConversationStatus = "active" | "completed";
export type Sender = "user" | "assistant";

export interface UserProfile {
  id: string | null;
  user_id: string | null;
  common_mistakes: string[];
  grammar_focus_areas: string[];
  vocabulary_gaps: string[];
  strengths: string[];
  last_feedback_summary: string | null;
  created_at: string | null;
  updated_at: string | null;
}

export interface User {
  id: string;
  email: string;
  plan: Plan;
  german_level: string | null;
  native_language: string | null;
  user_profile: UserProfile;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  user: User;
}

export interface ScenarioRole {
  id: string;
  scenario_id: string;
  role_name: string;
  prompt_context: string;
  created_at?: string;
}

export interface Scenario {
  id: string;
  name: string;
  description: string | null;
  prompt_context: string;
  is_premium: boolean;
  created_at: string;
  roles: ScenarioRole[];
}

export interface Message {
  id: string;
  conversation_id: string;
  sender: Sender;
  message_type: string;
  content: string;
  transcript?: string | null;
  audio_url?: string | null;
  created_at: string;
}

export interface Mistake {
  span: string;
  issue: string;
  category: string;
}

export interface MessageFeedback {
  id: string;
  feedback_session_id: string;
  message_id: string;
  original_text: string;
  corrected_text: string;
  mistakes: Mistake[];
  better_alternatives: string[];
  explanations: string[];
  created_at: string;
}

export interface FeedbackSession {
  id: string;
  conversation_id: string;
  overall_feedback: string | null;
  created_at: string;
  message_feedback: MessageFeedback[];
}

export interface ConversationListItem {
  id: string;
  user_id: string;
  scenario_id: string;
  scenario_role_id: string;
  status: ConversationStatus;
  started_at: string;
  ended_at: string | null;
  scenario_name: string;
  user_role_name: string;
  ai_role_name: string | null;
  user_message_count: number;
}

export interface ConversationDetail extends ConversationListItem {
  email: string;
  user_plan: string;
  german_level: string | null;
  native_language: string | null;
  user_profile: UserProfile;
  scenario_description: string | null;
  scenario_prompt_context: string;
  is_premium: boolean;
  user_role_prompt_context: string | null;
  ai_role_prompt_context: string | null;
  user_role: ScenarioRole | null;
  ai_role: ScenarioRole | null;
  conversation_summary: string | null;
  summary_updated_at: string | null;
  messages: Message[];
  feedback: FeedbackSession | null;
  opening_message_error?: string;
}

export interface ConversationTurnResponse {
  user_message: Message;
  assistant_message: Message;
}

export interface InlineFeedbackResponse {
  feedback_session_id: string;
  feedback_summary: string;
  message_feedback: MessageFeedback;
}

export interface CompleteConversationResponse {
  feedback_session: Omit<FeedbackSession, "message_feedback">;
  message_feedback: MessageFeedback[];
  user_profile: UserProfile | null;
  profile_update_error: string | null;
  final_feedback_error: string | null;
}

export interface ApiErrorPayload {
  error: string;
  user_message?: Message;
}
