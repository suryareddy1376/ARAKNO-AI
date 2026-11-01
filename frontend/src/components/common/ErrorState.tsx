import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

interface ErrorStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
  className?: string;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  title = 'Failed to load records',
  message = 'An error occurred during data retrieval.',
  onRetry,
  className = '',
}) => {
  return (
    <div className={`flex flex-col items-center justify-center py-12 px-4 text-center rounded-lg border border-red-900/30 bg-red-950/10 ${className}`}>
      <AlertTriangle className="w-8 h-8 text-red-400 mb-3" />
      <h3 className="text-base font-medium text-red-200 mb-1">{title}</h3>
      <p className="text-sm text-gray-400 max-w-md mb-4">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="inline-flex items-center gap-2 px-3 py-1.5 rounded bg-red-900/30 hover:bg-red-900/50 text-red-200 text-xs font-medium transition"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          Retry
        </button>
      )}
    </div>
  );
};
