import api from './api';
import { ResearchJob, ResearchRunRequest } from '../types/research';

export const startResearchRun = async (req: ResearchRunRequest): Promise<ResearchJob> => {
  const resp = await api.post('/research/run', req);
  return resp.data;
};

export const getResearchJobs = async (status?: string): Promise<ResearchJob[]> => {
  const resp = await api.get('/research/jobs', { params: { status } });
  return resp.data;
};

export const getResearchJob = async (jobId: string): Promise<ResearchJob> => {
  const resp = await api.get(`/research/jobs/${jobId}`);
  return resp.data;
};

export const getResearchJobResults = async (jobId: string) => {
  const resp = await api.get(`/research/jobs/${jobId}/results`);
  return resp.data;
};

export const cancelResearchJob = async (jobId: string) => {
  const resp = await api.post(`/research/jobs/${jobId}/cancel`);
  return resp.data;
};
