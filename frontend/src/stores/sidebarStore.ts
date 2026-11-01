import { create } from 'zustand';

interface SidebarState {
  isCollapsed: boolean;
  toggleCollapse: () => void;
  setCollapsed: (collapsed: boolean) => void;
}

export const useSidebarStore = create<SidebarState>((set) => ({
  isCollapsed: localStorage.getItem('arakno-sidebar') === 'true',
  toggleCollapse: () =>
    set((state) => {
      const next = !state.isCollapsed;
      localStorage.setItem('arakno-sidebar', String(next));
      return { isCollapsed: next };
    }),
  setCollapsed: (collapsed) => {
    localStorage.setItem('arakno-sidebar', String(collapsed));
    set({ isCollapsed: collapsed });
  },
}));
