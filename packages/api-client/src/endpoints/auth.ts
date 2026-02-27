import { apiClient } from '../client';
import type { LoginRequest, UserCreate, UserResponse, TokenResponse } from '@ecotrack/types';

export const authApi = {
  login: async (data: LoginRequest) => {
    const response = await apiClient.post<TokenResponse>('/api/v1/auth/login', data);
    return response.data;
  },

  register: async (data: UserCreate) => {
    const response = await apiClient.post<UserResponse>('/api/v1/auth/register', data);
    return response.data;
  },

  me: async () => {
    const response = await apiClient.get<UserResponse>('/api/v1/auth/me');
    return response.data;
  },
};
