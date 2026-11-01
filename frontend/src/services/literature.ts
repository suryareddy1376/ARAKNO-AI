import api from './api';
import { Publication, PublicationSearchParams, PublicationSearchResult } from '../types/literature';
import { PaginatedResponse } from '../types/api';

export const searchLiterature = async (params: {
  query: string;
  source?: string;
  max_results?: number;
  year_start?: number;
  year_end?: number;
  open_access_only?: boolean;
}): Promise<PublicationSearchResult[]> => {
  const resp = await api.post('/literature/search', params);
  return resp.data;
};

export const getSavedPublications = async (params?: {
  query?: string;
  project_id?: string;
  page?: number;
  page_size?: number;
}): Promise<PaginatedResponse<Publication>> => {
  const resp = await api.get('/literature', { params });
  return resp.data;
};

export const savePublication = async (pub: Partial<Publication>): Promise<Publication> => {
  const resp = await api.post('/literature/save', pub);
  return resp.data;
};

export const deletePublication = async (paperId: string): Promise<void> => {
  await api.delete(`/literature/${paperId}`);
};

export const updatePublicationNotes = async (paperId: string, notes: string): Promise<Publication> => {
  const resp = await api.post(`/literature/${paperId}/notes`, { notes });
  return resp.data;
};
