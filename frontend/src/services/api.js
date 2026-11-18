import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || (
  typeof window !== 'undefined' && window.location.hostname === 'localhost'
    ? '/api'
    : 'https://multi-agent-system-fs68.onrender.com/api'
);

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercept requests to attach JWT token if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => Promise.reject(error));

// Authentication
export const authLogin = (email, password) => api.post('/auth/login', { email, password });
export const authRegister = (data) => api.post('/auth/register', data);
export const getMe = () => api.get('/auth/me');

// Business Profile
export const getProfile = () => api.get('/profile');
export const updateProfile = (data) => api.put('/profile', data);

// Dataset
export const getDatasetSummary = () => api.get('/dataset/summary');
export const getProperties = (params) => api.get('/dataset/properties', { params });
export const getLeads = (params) => api.get('/dataset/leads', { params });
export const getDeals = (params) => api.get('/dataset/deals', { params });
export const getSiteVisits = (params) => api.get('/dataset/visits', { params });
export const getExpenses = (params) => api.get('/dataset/expenses', { params });
export const uploadDatasetFile = (formData) => api.post('/dataset/upload', formData, {
  headers: { 'Content-Type': 'multipart/form-data' },
});

// Analytics & KPIs
export const getKPIs = () => api.get('/analytics/kpis');
export const getMonthlyTrends = () => api.get('/analytics/monthly-trends');
export const getCityPerformance = () => api.get('/analytics/city-performance');
export const getPropertyTypes = () => api.get('/analytics/property-types');
export const getLeadFunnel = () => api.get('/analytics/lead-funnel');
export const getLeadSources = () => api.get('/analytics/lead-sources');
export const getAgentLeaderboard = (limit = 15) => api.get(`/analytics/agent-leaderboard?limit=${limit}`);
export const getExpenseBreakdown = () => api.get('/analytics/expense-breakdown');

// Multi-Agent (CrewAI)
export const executeAgents = (payload) => api.post('/agents/execute', payload);
export const getAgentsStatus = () => api.get('/agents/status');
export const getAgentLogs = (runId) => api.get('/agents/logs', { params: { run_id: runId } });
export const getPreviousRuns = () => api.get('/agents/runs');

// Human-in-the-Loop Approvals
export const getApprovals = (status) => api.get('/approvals', { params: { status } });
export const recordApprovalDecision = (id, decision, reason) =>
  api.post(`/approvals/${id}/decision`, { decision, reason });

// Reports & PDF
export const getReports = () => api.get('/reports');
export const getReportDetails = (id) => api.get(`/reports/${id}`);
export const getReportPdfUrl = (id) => `${API_BASE}/reports/${id}/pdf`;

// AI Business Chat
export const sendChatMessage = (message) => api.post('/chat', { message });

export default api;
