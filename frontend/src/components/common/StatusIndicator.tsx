import React from 'react';

interface StatusIndicatorProps {
  status: 'online' | 'offline' | 'busy' | 'pending';
  label?: string;
  size?: 'sm' | 'md';
}

export const StatusIndicator: React.FC<StatusIndicatorProps> = ({
  status,
  label,
  size = 'sm',
}) => {
  const dotColors = {
    online: 'bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.5)]',
    offline: 'bg-rose-500',
    busy: 'bg-amber-500 animate-pulse',
    pending: 'bg-blue-500',
  };

  const dotSize = size === 'sm' ? 'w-2 h-2' : 'w-2.5 h-2.5';

  return (
    <div className="inline-flex items-center gap-2">
      <span className={`rounded-full ${dotSize} ${dotColors[status]}`} />
      {label && <span className="text-xs font-medium text-gray-300">{label}</span>}
    </div>
  );
};
