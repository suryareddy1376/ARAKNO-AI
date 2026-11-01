import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

import { AppLayout } from './components/layout/AppLayout';
import { DashboardPage } from './features/dashboard/DashboardPage';
import { ResearchLabPage } from './features/research-lab/ResearchLabPage';
import { LiteraturePage } from './features/literature/LiteraturePage';
import { ProteinExplorerPage } from './features/proteins/ProteinExplorerPage';
import { BiologyPage } from './features/biology/BiologyPage';
import { EvidencePage } from './features/evidence/EvidencePage';
import { DivisionsPage } from './features/divisions/DivisionsPage';
import { ProjectsPage } from './features/projects/ProjectsPage';
import { ReportsPage } from './features/reports/ReportsPage';
import { SettingsPage } from './features/settings/SettingsPage';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AppLayout />}>
          <Route index element={<DashboardPage />} />
          <Route path="research-lab" element={<ResearchLabPage />} />
          <Route path="literature" element={<LiteraturePage />} />
          <Route path="proteins" element={<ProteinExplorerPage />} />
          <Route path="biology" element={<BiologyPage />} />
          <Route path="evidence" element={<EvidencePage />} />
          <Route path="divisions" element={<DivisionsPage />} />
          <Route path="projects" element={<ProjectsPage />} />
          <Route path="reports" element={<ReportsPage />} />
          <Route path="settings" element={<SettingsPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default App;
