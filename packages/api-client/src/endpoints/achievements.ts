import { apiClient } from '../client';
import type { AchievementResponse, UserAchievementResponse } from '@ecotrack/types';

export const achievementsApi = {
  getAll: async () => {
    const response = await apiClient.get<AchievementResponse[]>('/api/v1/achievements');
    return response.data;
  },

  getUserAchievements: async () => {
    const response = await apiClient.get<UserAchievementResponse[]>('/api/v1/achievements/my-achievements');
    return response.data;
  },
};
