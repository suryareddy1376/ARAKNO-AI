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
    <div className="flex h-screen w-screen overflow-hidden bg-[#0f1117] text-[#e6edf3]">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <Header apiOnline={apiOnline} />
        <main className="flex-1 overflow-y-auto p-6 md:p-8">
          <Outlet />
        </main>
      </div>
      <ToastNotification />
    </div>
  );
};
