import api from './api';
import { ResearchProject, ResearchDivision, ResearchQuestion } from '../types/research';

export const getResearchDivisions = async (): Promise<ResearchDivision[]> => {
  const resp = await api.get('/projects/divisions');
  return resp.data;
};

export const getProjects = async (params?: { division_id?: number; status?: string }): Promise<ResearchProject[]> => {
  const resp = await api.get('/projects', { params });
  return resp.data;
};

export const getProject = async (projectId: string): Promise<ResearchProject> => {
  const resp = await api.get(`/projects/${projectId}`);
  return resp.data;
};

export const createProject = async (projectData: Partial<ResearchProject>): Promise<ResearchProject> => {
  const resp = await api.post('/projects', projectData);
  return resp.data;
};

export const updateProject = async (projectId: string, updates: Partial<ResearchProject>): Promise<ResearchProject> => {
  const resp = await api.patch(`/projects/${projectId}`, updates);
  return resp.data;
};

export const addProjectQuestion = async (projectId: string, question: { question: string; hypothesis?: string }): Promise<ResearchQuestion> => {
  const resp = await api.post(`/projects/${projectId}/questions`, {
    ...question,
    project_id: projectId,
  });
  return resp.data;
};
