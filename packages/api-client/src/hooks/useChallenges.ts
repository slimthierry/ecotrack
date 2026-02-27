import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { challengesApi } from '../endpoints/challenges';
import type { ChallengeJoin } from '@ecotrack/types';

export function useChallenges() {
  return useQuery({
    queryKey: ['challenges'],
    queryFn: () => challengesApi.getActive(),
    staleTime: 5 * 60 * 1000,
  });
}

export function useMyChallenges() {
  return useQuery({
    queryKey: ['challenges', 'mine'],
    queryFn: () => challengesApi.getMyChallenges(),
    staleTime: 2 * 60 * 1000,
  });
}

export function useJoinChallenge() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: ChallengeJoin) => challengesApi.join(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['challenges'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
    },
  });
}

export function useLeaderboard(challengeId: string, limit = 20) {
  return useQuery({
    queryKey: ['challenges', 'leaderboard', challengeId, limit],
    queryFn: () => challengesApi.getLeaderboard(challengeId, limit),
    staleTime: 2 * 60 * 1000,
    enabled: !!challengeId,
  });
}
