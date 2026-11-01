import React from 'react';
import { LucideIcon } from 'lucide-react';

interface StatCardProps {
  title: string;
  value: number | string;
  subtitle?: string;
  icon: LucideIcon;
  color?: string;
  trend?: string;
}

export const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  color = '#3b82f6',
  trend,
}) => {
  return (
    <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-4 flex flex-col justify-between hover:border-gray-600 transition">
      <div className="flex items-center justify-between">
        <span className="text-xs font-medium text-[#8b949e] uppercase tracking-wider">{title}</span>
        <div
          className="w-8 h-8 rounded flex items-center justify-center"
          style={{ backgroundColor: `${color}18`, color }}
        >
          <Icon className="w-4 h-4" />
        </div>
      </div>
      <div className="mt-2">
        <span className="text-2xl font-bold tracking-tight text-[#e6edf3]">{value}</span>
        {subtitle && <p className="text-xs text-[#8b949e] mt-0.5">{subtitle}</p>}
        {trend && <span className="text-xs text-emerald-400 font-medium mt-1 inline-block">{trend}</span>}
      </div>
    </div>
  );
};
