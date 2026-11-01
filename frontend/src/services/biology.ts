import api from './api';
import { FastaAnalysisResponse, SequenceComparisonResponse, StructureAnalysisResponse } from '../types/biology';

export const analyzeFastaText = async (fastaText: string, sequenceType: string = 'protein'): Promise<FastaAnalysisResponse> => {
  const resp = await api.post('/biology/fasta/analyze', {
    fasta_text: fastaText,
    sequence_type: sequenceType,
  });
  return resp.data;
};

export const compareSequences = async (
  seq1: string,
  seq2: string,
  comparisonType: string = 'global'
): Promise<SequenceComparisonResponse> => {
  const resp = await api.post('/biology/sequences/compare', {
    seq1,
    seq2,
    comparison_type: comparisonType,
  });
  return resp.data;
};

export const analyzeStructureFile = async (file: File, format: string = 'pdb'): Promise<StructureAnalysisResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('format', format);
  const resp = await api.post('/biology/structures/analyze', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return resp.data;
};
