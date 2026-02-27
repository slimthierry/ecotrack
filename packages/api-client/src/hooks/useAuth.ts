import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { authApi } from '../endpoints/auth';
import type { LoginRequest, UserCreate } from '@ecotrack/types';

export function useLogin() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (data: LoginRequest) => {
      const tokens = await authApi.login(data);
      localStorage.setItem('access_token', tokens.access_token);
      return tokens;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['auth'] });
    },
  });
}

export function useRegister() {
  return useMutation({
    mutationFn: (data: UserCreate) => authApi.register(data),
  });
}

export function useCurrentUser() {
  return useQuery({
    queryKey: ['auth', 'me'],
    queryFn: () => authApi.me(),
    staleTime: 5 * 60 * 1000,
    retry: false,
  });
}
