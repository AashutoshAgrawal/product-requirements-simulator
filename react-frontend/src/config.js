/**
 * Application Configuration
 * Centralized configuration for API endpoints and other settings
 */

const config = {
  // Backend API URL - automatically detects environment
  apiUrl: process.env.REACT_APP_API_URL || 
          (process.env.NODE_ENV === 'production' 
            ? 'https://elicitron-backend.onrender.com'
            : 'http://localhost:8000'),
  
  // API endpoints
  endpoints: {
    analyze: '/api/analyze',
    health: '/api/health',
  },
  
  // App settings
  app: {
    name: 'Elicitron',
    version: '2.0.0',
  }
};

export default config;
