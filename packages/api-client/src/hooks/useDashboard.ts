import { useQuery } from '@tanstack/react-query';
import { dashboardApi } from '../endpoints/dashboard';

export function useDashboard() {
  return useQuery({
    queryKey: ['dashboard', 'overview'],
    queryFn: () => dashboardApi.getOverview(),
    staleTime: 2 * 60 * 1000,
    refetchInterval: 5 * 60 * 1000,
  });
}

export function useTrends() {
  return useQuery({
    queryKey: ['dashboard', 'trends'],
    queryFn: () => dashboardApi.getTrends(),
    staleTime: 2 * 60 * 1000,
  });
}

export function useBreakdown(days = 30) {
  return useQuery({
    queryKey: ['dashboard', 'breakdown', days],
    queryFn: () => dashboardApi.getBreakdown(days),
    staleTime: 2 * 60 * 1000,
  });
}

export function useEcoTips(category?: string) {
  return useQuery({
    queryKey: ['dashboard', 'tips', category],
    queryFn: () => dashboardApi.getTips(category),
    staleTime: 10 * 60 * 1000,
  });
}
