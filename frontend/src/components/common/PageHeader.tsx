import React, { ReactNode } from 'react';

interface PageHeaderProps {
  title: string;
  subtitle?: string;
  badge?: string;
  actions?: ReactNode;
}

export const PageHeader: React.FC<PageHeaderProps> = ({
  title,
  subtitle,
  badge,
  actions,
}) => {
  return (
    <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 pb-6 border-b border-[#30363d]/60 mb-6">
      <div>
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-bold tracking-tight text-[#e6edf3]">{title}</h1>
          {badge && (
            <span className="px-2.5 py-0.5 rounded text-xs font-semibold uppercase tracking-wider bg-blue-900/40 text-blue-300 border border-blue-700/50">
              {badge}
            </span>
          )}
        </div>
        {subtitle && <p className="text-sm text-[#8b949e] mt-1">{subtitle}</p>}
      </div>
      {actions && <div className="flex items-center gap-2.5">{actions}</div>}
    </div>
  );
};
