import React from 'react';
import { CheckCircle2, AlertCircle, Info, X } from 'lucide-react';
import { useNotificationStore } from '../../stores/notificationStore';

export const ToastNotification: React.FC = () => {
  const { toasts, removeToast } = useNotificationStore();

  if (toasts.length === 0) return null;

  return (
    <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2 max-w-sm w-full pointer-events-none">
      {toasts.map((toast) => {
        const icons = {
          success: <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />,
          error: <AlertCircle className="w-4 h-4 text-rose-400 shrink-0" />,
          warning: <AlertCircle className="w-4 h-4 text-amber-400 shrink-0" />,
          info: <Info className="w-4 h-4 text-blue-400 shrink-0" />,
        };

        const bg = {
          success: 'border-emerald-800/50 bg-[#161b22]',
          error: 'border-rose-800/50 bg-[#161b22]',
          warning: 'border-amber-800/50 bg-[#161b22]',
          info: 'border-blue-800/50 bg-[#161b22]',
        };

        return (
          <div
            key={toast.id}
            className={`pointer-events-auto flex items-start gap-3 p-3 rounded-lg border shadow-lg text-sm text-[#e6edf3] ${bg[toast.type]}`}
          >
            {icons[toast.type]}
            <div className="flex-1">
              {toast.title && <h4 className="font-semibold text-xs mb-0.5">{toast.title}</h4>}
              <p className="text-xs text-[#8b949e]">{toast.message}</p>
            </div>
            <button
              onClick={() => removeToast(toast.id)}
              className="text-gray-400 hover:text-white transition"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </div>
        );
      })}
    </div>
  );
};
