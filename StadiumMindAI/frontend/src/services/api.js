import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 15000,
});

apiClient.interceptors.request.use(config => {
  config.headers['Accept'] = 'application/json';
  return config;
});

apiClient.interceptors.response.use(
  response => response.data,
  error => Promise.reject(error)
);

// Crowd
export const getCrowdHeatmap = () => apiClient.get('/api/crowd/heatmap');
export const getCrowdAlerts = () => apiClient.get('/api/crowd/alerts');
export const getCrowdStats = () => apiClient.get('/api/crowd/stats');
export const getCrowdZone = (zoneId) => apiClient.get(`/api/crowd/zone/${zoneId}`);

// Volunteers
export const getVolunteers = () => apiClient.get('/api/volunteers');
export const getVolunteerGaps = () => apiClient.get('/api/volunteers/gaps');
export const assignTasks = (data) => apiClient.post('/api/volunteers/tasks', data);

// Incidents
export const getIncidents = () => apiClient.get('/api/incidents');
export const getWeatherAdvisory = () => apiClient.get('/api/incidents/weather');
export const reportIncident = (data) => apiClient.post('/api/incidents', data);

// AI
export const askAI = (data) => apiClient.post('/api/ai/ask', data);
export const translateText = (data) => apiClient.post('/api/ai/translate', data);
export const getEmergencyResponse = (data) => apiClient.post('/api/ai/emergency', data);

// Dashboard
export const getDashboardSummary = () => apiClient.get('/api/dashboard/summary');
export const getDashboardKPIs = () => apiClient.get('/api/dashboard/kpis');
export const getMatchData = () => apiClient.get('/api/dashboard/match');
