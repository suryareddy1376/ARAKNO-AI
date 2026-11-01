import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  FlaskConical,
  BookOpen,
  Atom,
  Dna,
  FileCheck,
  Building2,
  FolderKanban,
  FileText,
  Settings,
  ChevronLeft,
  ChevronRight,
  ShieldCheck,
} from 'lucide-react';
import { useSidebarStore } from '../../stores/sidebarStore';

const navItems = [
  { label: 'Dashboard', path: '/', icon: LayoutDashboard },
  { label: 'Research lab', path: '/research-lab', icon: FlaskConical },
  { label: 'Literature explorer', path: '/literature', icon: BookOpen },
  { label: 'Protein explorer', path: '/proteins', icon: Atom },
  { label: 'Computational biology', path: '/biology', icon: Dna },
  { label: 'Evidence library', path: '/evidence', icon: FileCheck },
  { label: 'Research divisions', path: '/divisions', icon: Building2 },
  { label: 'Research projects', path: '/projects', icon: FolderKanban },
  { label: 'Reports', path: '/reports', icon: FileText },
  { label: 'Settings', path: '/settings', icon: Settings },
];

export const Sidebar: React.FC = () => {
  const { isCollapsed, toggleCollapse } = useSidebarStore();

  return (
    <aside
      className={`relative flex flex-col border-r border-[#30363d] bg-[#161b22] transition-all duration-300 z-20 shrink-0 ${
        isCollapsed ? 'w-16' : 'w-64'
      }`}
    >
      {/* Brand Header */}
      <div className="flex items-center justify-between h-16 px-4 border-b border-[#30363d]">
        {!isCollapsed && (
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-600 to-cyan-600 flex items-center justify-center text-white font-black text-sm shadow-md">
              A
            </div>
            <div>
              <span className="font-extrabold text-sm tracking-wider text-[#e6edf3]">ARAKNO-AI</span>
              <span className="block text-[10px] text-[#8b949e] font-mono leading-none">RESEARCH PLATFORM</span>
            </div>
          </div>
        )}
        {isCollapsed && (
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-600 to-cyan-600 flex items-center justify-center text-white font-black text-sm mx-auto shadow-md">
            A
          </div>
        )}
        <button
          onClick={toggleCollapse}
          className={`p-1.5 rounded text-gray-400 hover:text-white hover:bg-gray-800 transition ${
            isCollapsed ? 'hidden' : 'block'
          }`}
          title="Toggle Sidebar"
        >
          <ChevronLeft className="w-4 h-4" />
        </button>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 overflow-y-auto py-4 px-2 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-md text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-blue-600/15 text-blue-400 border border-blue-500/30'
                    : 'text-[#8b949e] hover:text-[#e6edf3] hover:bg-[#21262d]'
                } ${isCollapsed ? 'justify-center px-0' : ''}`
              }
              title={isCollapsed ? item.label : undefined}
            >
              <Icon className="w-4 h-4 shrink-0" />
              {!isCollapsed && <span>{item.label}</span>}
            </NavLink>
          );
        })}
      </nav>

      {/* Privacy / Platform Badge */}
      <div className="p-3 border-t border-[#30363d] text-xs text-[#8b949e]">
        {!isCollapsed ? (
          <div className="flex items-center gap-2 px-2 py-1.5 rounded bg-[#0f1117]/60 border border-[#30363d]/50">
            <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0" />
            <div>
              <span className="block text-[11px] font-semibold text-[#e6edf3]">Local execution</span>
              <span className="text-[10px] text-gray-400">Local storage, no remote API cost</span>
            </div>
          </div>
        ) : (
          <div className="flex justify-center" title="Local execution">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
          </div>
        )}
      </div>
    </aside>
  );
};
