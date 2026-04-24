import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { api } from "@/api/client";
import { useAuth } from "@/providers/AuthProvider";

export function useConversationsQuery() {
  const { token } = useAuth();
  return useQuery({
    queryKey: ["conversations"],
    queryFn: () => api.conversations(token!),
    enabled: Boolean(token)
  });
}

export function useConversationQuery(conversationId?: string) {
  const { token } = useAuth();
  return useQuery({
    queryKey: ["conversation", conversationId],
    queryFn: ({ signal }) => api.conversation(token!, conversationId!, signal),
    enabled: Boolean(token && conversationId)
  });
}

export function useCreateConversationMutation() {
  const { token } = useAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: { scenario_id: string; scenario_role_id: string; generate_opening_message?: boolean }) =>
      api.createConversation(token!, payload),
    onSuccess: (conversation) => {
      queryClient.invalidateQueries({ queryKey: ["conversations"] });
      queryClient.setQueryData(["conversation", conversation.id], conversation);
    }
  });
}

export function useSendMessageMutation(conversationId: string) {
  const { token } = useAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (content: string) => api.sendMessage(token!, conversationId, content),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["conversation", conversationId] });
      queryClient.invalidateQueries({ queryKey: ["conversations"] });
    }
  });
}

export function useInlineFeedbackMutation(conversationId: string) {
  const { token } = useAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (messageId: string) => api.messageFeedback(token!, conversationId, messageId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["conversation", conversationId] });
      queryClient.invalidateQueries({ queryKey: ["conversation-feedback", conversationId] });
    }
  });
}

export function useConversationFeedbackQuery(conversationId?: string) {
  const { token } = useAuth();
  return useQuery({
    queryKey: ["conversation-feedback", conversationId],
    queryFn: () => api.conversationFeedback(token!, conversationId!),
    enabled: Boolean(token && conversationId)
  });
}

export function useCompleteConversationMutation(conversationId: string) {
  const { token } = useAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: () => api.completeConversation(token!, conversationId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["conversation", conversationId] });
      queryClient.invalidateQueries({ queryKey: ["conversations"] });
      queryClient.invalidateQueries({ queryKey: ["conversation-feedback", conversationId] });
    }
  });
}
