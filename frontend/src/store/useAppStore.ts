import { create } from 'zustand';

export type AppMode = 'read' | 'compose' | 'loading';

interface AppState {
  mode: AppMode;
  isInitialized: boolean;
  accessToken: string | null;
  error: string | null;
  
  setMode: (mode: AppMode) => void;
  setInitialized: (initialized: boolean) => void;
  setAccessToken: (token: string) => void;
  setError: (error: string | null) => void;
}

export const useAppStore = create<AppState>((set) => ({
  mode: 'loading',
  isInitialized: false,
  accessToken: null,
  error: null,
  
  setMode: (mode) => set({ mode }),
  setInitialized: (isInitialized) => set({ isInitialized }),
  setAccessToken: (accessToken) => set({ accessToken }),
  setError: (error) => set({ error }),
}));
