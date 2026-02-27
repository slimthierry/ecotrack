import { apiClient } from '../client';
import type { DashboardOverview, WeeklyTrend, CategoryBreakdown, EcoTip } from '@ecotrack/types';

export const dashboardApi = {
  getOverview: async () => {
    const response = await apiClient.get<DashboardOverview>('/api/v1/dashboard/overview');
    return response.data;
  },

  getTrends: async () => {
    const response = await apiClient.get<WeeklyTrend>('/api/v1/dashboard/trends');
    return response.data;
  },

  getBreakdown: async (days = 30) => {
    const response = await apiClient.get<CategoryBreakdown>('/api/v1/dashboard/breakdown', {
      params: { days },
    });
    return response.data;
  },

  getTips: async (category?: string) => {
    const response = await apiClient.get<EcoTip[]>('/api/v1/dashboard/tips', {
      params: category ? { category } : undefined,
    });
    return response.data;
  },
};
