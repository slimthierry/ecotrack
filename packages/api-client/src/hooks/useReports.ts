import { useQuery } from '@tanstack/react-query';
import { reportsApi } from '../endpoints/reports';

export function useWeeklyReport() {
  return useQuery({
    queryKey: ['reports', 'weekly'],
    queryFn: () => reportsApi.getWeekly(),
    staleTime: 5 * 60 * 1000,
  });
}

export function useMonthlyReport() {
  return useQuery({
    queryKey: ['reports', 'monthly'],
    queryFn: () => reportsApi.getMonthly(),
    staleTime: 5 * 60 * 1000,
  });
}
