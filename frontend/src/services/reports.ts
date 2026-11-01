import api from './api';
import { ResearchReport, ResearchReportCreate } from '../types/reports';

export const getReports = async (projectId?: string): Promise<ResearchReport[]> => {
  const resp = await api.get('/reports', { params: { project_id: projectId } });
  return resp.data;
};

export const getReport = async (reportId: string): Promise<ResearchReport> => {
  const resp = await api.get(`/reports/${reportId}`);
  return resp.data;
};

export const createReport = async (reportData: ResearchReportCreate): Promise<ResearchReport> => {
  const resp = await api.post('/reports/generate', reportData);
  return resp.data;
};

export const deleteReport = async (reportId: string): Promise<void> => {
  await api.delete(`/reports/${reportId}`);
};
