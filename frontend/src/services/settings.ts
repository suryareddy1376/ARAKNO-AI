import api from './api';
import { SystemSettings, ProviderStatus } from '../types/settings';

export const getSystemSettings = async (): Promise<SystemSettings> => {
  const resp = await api.get('/settings');
  return resp.data;
};

export const updateSystemSettings = async (settings: Partial<SystemSettings>): Promise<SystemSettings> => {
  const resp = await api.patch('/settings', settings);
  return resp.data;
};

export const getProviderStatus = async (): Promise<ProviderStatus[]> => {
  const resp = await api.get('/settings/provider-status');
  return resp.data;
};
