import { create } from 'zustand';

interface ThemeState {
  theme: 'dark' | 'light';
  toggleTheme: () => void;
  setTheme: (theme: 'dark' | 'light') => void;
}

export const useThemeStore = create<ThemeState>((set) => {
  const savedTheme = (localStorage.getItem('arakno-theme') as 'dark' | 'light') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);

  return {
    theme: savedTheme,
    toggleTheme: () =>
      set((state) => {
        const next = state.theme === 'dark' ? 'light' : 'dark';
        localStorage.setItem('arakno-theme', next);
        document.documentElement.setAttribute('data-theme', next);
        return { theme: next };
      }),
    setTheme: (theme) => {
      localStorage.setItem('arakno-theme', theme);
      document.documentElement.setAttribute('data-theme', theme);
      set({ theme });
    },
  };
});
