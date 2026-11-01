import React from 'react';
import { Sun, Moon, Database, Search, Activity } from 'lucide-react';
import { useThemeStore } from '../../stores/themeStore';
import { StatusIndicator } from '../common/StatusIndicator';

interface HeaderProps {
  apiOnline?: boolean;
}

export const Header: React.FC<HeaderProps> = ({ apiOnline = true }) => {
  const { theme, toggleTheme } = useThemeStore();

  return (
    <header className="h-16 border-b border-[#30363d] bg-[#161b22] px-6 flex items-center justify-between z-10">
      {/* Global Search Bar */}
      <div className="relative w-80">
        <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
        <input
          type="text"
          placeholder="Search publications, proteins, or evidence..."
          className="w-full bg-[#0f1117] border border-[#30363d] rounded-md pl-9 pr-3 py-1.5 text-xs text-[#e6edf3] placeholder-gray-500 focus:border-blue-500 focus:outline-none transition"
        />
      </div>

      {/* Status and Controls */}
      <div className="flex items-center gap-4">
        {/* Backend Connectivity Status */}
        <div className="flex items-center gap-2 px-2.5 py-1 rounded bg-[#0f1117] border border-[#30363d]">
          <StatusIndicator status={apiOnline ? 'online' : 'offline'} />
          <span className="text-xs text-[#8b949e]">
            {apiOnline ? 'Backend connected' : 'Backend offline'}
          </span>
        </div>

        {/* Database Status */}
        <div className="flex items-center gap-1.5 text-xs text-[#8b949e]">
          <Database className="w-3.5 h-3.5 text-blue-400" />
          <span>SQLite connected</span>
        </div>

        {/* Theme Toggle */}
        <button
          onClick={toggleTheme}
          className="p-1.5 rounded text-gray-400 hover:text-white hover:bg-gray-800 transition"
          title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
        >
          {theme === 'dark' ? <Sun className="w-4 h-4 text-amber-300" /> : <Moon className="w-4 h-4" />}
        </button>
      </div>
    </header>
  );
};
