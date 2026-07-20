import axios from 'axios';
import { useAppStore } from '../store/useAppStore';

const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/ai';

export const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to attach the SSO token
apiClient.interceptors.request.use((config) => {
  const token = useAppStore.getState().accessToken;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});
