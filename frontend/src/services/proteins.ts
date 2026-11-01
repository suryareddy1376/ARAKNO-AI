import api from './api';
import { Protein, ProteinStructure } from '../types/proteins';

export const resolveProteinAccession = async (query: string) => {
  const resp = await api.post('/proteins/resolve-accession', { query });
  return resp.data;
};

export const getProteinDetails = async (accession: string): Promise<Protein> => {
  const resp = await api.get(`/proteins/${accession}`);
  return resp.data;
};

export const getProteinStructures = async (accession: string) => {
  const resp = await api.get(`/proteins/${accession}/structures`);
  return resp.data;
};

export const downloadProteinStructure = async (accession: string, format: string = 'pdb') => {
  const resp = await api.post(`/proteins/${accession}/download`, null, { params: { format } });
  return resp.data;
};

export const getStructureFileContent = async (accession: string): Promise<string> => {
  const resp = await api.get(`/proteins/${accession}/structure-content`, { responseType: 'text' });
  return resp.data;
};

export const saveProtein = async (proteinData: Partial<Protein>): Promise<Protein> => {
  const resp = await api.post('/proteins/save', proteinData);
  return resp.data;
};
