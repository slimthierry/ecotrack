import { apiClient } from '../client';
import type { WeeklyReport, MonthlyReport } from '@ecotrack/types';

export const reportsApi = {
  getWeekly: async () => {
    const response = await apiClient.get<WeeklyReport>('/api/v1/reports/weekly');
    return response.data;
  },

  getMonthly: async () => {
    const response = await apiClient.get<MonthlyReport>('/api/v1/reports/monthly');
    return response.data;
  },
};
