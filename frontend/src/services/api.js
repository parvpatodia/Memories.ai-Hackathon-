import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 second timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add timestamp to prevent caching issues
    config.params = {
      ...config.params,
      _t: Date.now()
    };
    
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ API Error:', error.response?.data || error.message);
    
    // Handle different error types
    if (error.code === 'ECONNABORTED') {
      throw new Error('Request timeout - please check your connection and try again');
    }
    
    if (error.response) {
      // Server responded with error status
      const errorMessage = error.response.data?.message || 
                          error.response.data?.detail || 
                          `Server error (${error.response.status})`;
      throw new Error(errorMessage);
    } else if (error.request) {
      // Network error
      throw new Error('Network error - please check your connection');
    } else {
      // Other error
      throw new Error(error.message || 'An unexpected error occurred');
    }
  }
);

// API methods with better error handling
export const checkHealth = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error.message);
    throw new Error('Unable to connect to server');
  }
};

export const uploadVideo = async (file) => {
  if (!file) {
    throw new Error('No file provided');
  }
  
  if (!file.type.startsWith('video/')) {
    throw new Error('Please select a video file');
  }
  
  if (file.size > 50 * 1024 * 1024) {
    throw new Error('File size must be less than 50MB');
  }
  
  const formData = new FormData();
  formData.append('file', file);
  
  try {
    const response = await api.post('/api/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 120000, // 2 minute timeout for uploads
      onUploadProgress: (progressEvent) => {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        console.log(`Upload progress: ${percentCompleted}%`);
      }
    });
    
    return response.data;
  } catch (error) {
    if (error.message.includes('timeout')) {
      throw new Error('Upload timeout - please try with a smaller file');
    }
    throw error;
  }
};

export const teachObject = async (name, alias) => {
  if (!name || !alias) {
    throw new Error('Both object name and description are required');
  }
  
  if (name.length > 100) {
    throw new Error('Object name must be less than 100 characters');
  }
  
  if (alias.length > 500) {
    throw new Error('Object description must be less than 500 characters');
  }
  
  const response = await api.post('/api/objects/', {
    name: name.trim(),
    alias: alias.trim()
  });
  
  return response.data;
};

export const getTrackedObjects = async () => {
  const response = await api.get('/api/objects/');
  return response.data;
};

export const deleteTrackedObject = async (objectId) => {
  if (!objectId) {
    throw new Error('Object ID is required');
  }
  
  const response = await api.delete(`/api/objects/${objectId}`);
  return response.data;
};

export const searchForObject = async (query) => {
  if (!query || query.trim().length === 0) {
    throw new Error('Search query cannot be empty');
  }
  
  if (query.length > 200) {
    throw new Error('Search query is too long');
  }
  
  const response = await api.post('/api/search/', {
    query: query.trim()
  });
  
  return response.data;
};

export const getSearchHistory = async () => {
  const response = await api.get('/api/search/history');
  return response.data;
};

export const getSearchSuggestions = async () => {
  const response = await api.get('/api/search/suggestions');
  return response.data;
};

export const getCommonObjects = async () => {
  const response = await api.get('/api/objects/suggestions/common');
  return response.data;
};

export default api;
