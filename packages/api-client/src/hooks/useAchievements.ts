import { useQuery } from '@tanstack/react-query';
import { achievementsApi } from '../endpoints/achievements';

export function useAchievements() {
  return useQuery({
    queryKey: ['achievements'],
    queryFn: () => achievementsApi.getAll(),
    staleTime: 10 * 60 * 1000,
  });
}

export function useUserAchievements() {
  return useQuery({
    queryKey: ['achievements', 'mine'],
    queryFn: () => achievementsApi.getUserAchievements(),
    staleTime: 2 * 60 * 1000,
  });
}
