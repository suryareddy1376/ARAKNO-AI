import api from './api';
import { EvidenceRecord, EvidenceSearchParams, CitationVerificationResult } from '../types/evidence';
import { PaginatedResponse } from '../types/api';

export const getEvidenceRecords = async (params?: Partial<EvidenceSearchParams>): Promise<PaginatedResponse<EvidenceRecord>> => {
  const resp = await api.get('/evidence', { params });
  return resp.data;
};

export const createEvidenceRecord = async (record: Partial<EvidenceRecord>): Promise<EvidenceRecord> => {
  const resp = await api.post('/evidence', record);
  return resp.data;
};

export const updateEvidenceRecord = async (id: string, updates: Partial<EvidenceRecord>): Promise<EvidenceRecord> => {
  const resp = await api.put(`/evidence/${id}`, updates);
  return resp.data;
};

export const verifyCitation = async (req: {
  doi?: string;
  pmid?: string;
  title?: string;
}): Promise<CitationVerificationResult> => {
  const resp = await api.post('/evidence/verify-citation', req);
  return resp.data;
};
