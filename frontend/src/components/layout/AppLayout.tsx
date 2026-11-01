import React, { useState, useEffect } from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { ToastNotification } from '../common/ToastNotification';
import { getSystemStatus } from '../../services/dashboard';

export const AppLayout: React.FC = () => {
  const [apiOnline, setApiOnline] = useState(true);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        await getSystemStatus();
        setApiOnline(true);
      } catch {
        setApiOnline(false);
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-[#0f1117] text-[#e6edf3] print:h-auto print:w-full print:overflow-visible print:bg-white print:text-black print:block">
      <div className="print:hidden">
        <Sidebar />
      </div>
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden print:overflow-visible print:h-auto print:block">
        <div className="print:hidden">
          <Header apiOnline={apiOnline} />
        </div>
        <main className="flex-1 overflow-y-auto p-6 md:p-8 print:p-0 print:overflow-visible print:h-auto print:block">
          <Outlet />
        </main>
      </div>
      <div className="print:hidden">
        <ToastNotification />
      </div>
    </div>
  );
};
