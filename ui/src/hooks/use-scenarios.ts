import { useMutation, useQuery } from "@tanstack/react-query";

import { api } from "@/api/client";
import type { Scenario } from "@/types/api";

export function useScenariosQuery() {
  return useQuery<Scenario[]>({
    queryKey: ["scenarios"],
    queryFn: api.scenarios
  });
}

export function useScenarioQuery(scenarioId?: string) {
  return useQuery({
    queryKey: ["scenario", scenarioId],
    queryFn: () => api.scenario(scenarioId!),
    enabled: Boolean(scenarioId)
  });
}

export function useScenarioRolesQuery(scenarioId?: string) {
  return useQuery({
    queryKey: ["scenario-roles", scenarioId],
    queryFn: () => api.scenarioRoles(scenarioId!),
    enabled: Boolean(scenarioId)
  });
}

export function useHealthCheck() {
  return useQuery({
    queryKey: ["health"],
    queryFn: api.health,
    staleTime: 60_000
  });
}
