import { apiClient } from '../client';
import type { ChallengeResponse, ChallengeJoin, ChallengeProgress, LeaderboardEntry } from '@ecotrack/types';

export const challengesApi = {
  getActive: async () => {
    const response = await apiClient.get<ChallengeResponse[]>('/api/v1/challenges');
    return response.data;
  },

  join: async (data: ChallengeJoin) => {
    const response = await apiClient.post<ChallengeProgress>('/api/v1/challenges/join', data);
    return response.data;
  },

  getMyChallenges: async () => {
    const response = await apiClient.get<ChallengeProgress[]>('/api/v1/challenges/my-challenges');
    return response.data;
  },

  getLeaderboard: async (challengeId: string, limit = 20) => {
    const response = await apiClient.get<LeaderboardEntry[]>(
      `/api/v1/challenges/leaderboard/${challengeId}`,
      { params: { limit } },
    );
    return response.data;
  },
};
