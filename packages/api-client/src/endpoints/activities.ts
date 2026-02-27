import { apiClient } from '../client';
import type { ActivityCreate, ActivityResponse, ActivitySummary } from '@ecotrack/types';

export const activitiesApi = {
  create: async (data: ActivityCreate) => {
    const response = await apiClient.post<ActivityResponse>('/api/v1/activities', data);
    return response.data;
  },

  list: async (params?: {
    category?: string;
    start_date?: string;
    end_date?: string;
    limit?: number;
    offset?: number;
  }) => {
    const response = await apiClient.get<ActivityResponse[]>('/api/v1/activities', { params });
    return response.data;
  },

  getSummary: async (params?: { start_date?: string; end_date?: string }) => {
    const response = await apiClient.get<ActivitySummary>('/api/v1/activities/summary', { params });
    return response.data;
  },

  delete: async (id: string) => {
    await apiClient.delete(`/api/v1/activities/${id}`);
  },
};
