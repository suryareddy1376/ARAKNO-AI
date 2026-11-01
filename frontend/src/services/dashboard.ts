import api from './api';
import { DashboardOverviewResponse } from '../types/dashboard';

export const getDashboardOverview = async (): Promise<DashboardOverviewResponse> => {
  const resp = await api.get('/dashboard/overview');
  return resp.data;
};

export const getSystemStatus = async () => {
  const resp = await api.get('/system/status');
  return resp.data;
};

export const getSystemStorage = async () => {
  const resp = await api.get('/system/storage');
  return resp.data;
};
