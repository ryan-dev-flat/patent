import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:5000/api',
});

// Request Interceptor to attach token to Authorization header
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response Interceptor for handling token refresh and 401 errors
axiosInstance.interceptors.response.use(
  (response) => response,  // Return the response as is if successful
  async (error) => {
    const originalRequest = error.config;
    
    // Prevent retrying the request if it's a login request or there's no refresh token
    if (originalRequest.url.includes('/login') || !localStorage.getItem('refreshToken')) {
      return Promise.reject(error);
    }

    // Handle 401 errors and refresh token logic for other requests
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        // Try refreshing the access token using the refresh token
        const refreshToken = localStorage.getItem('refreshToken');
        const response = await axiosInstance.post('/refresh_token', { token: refreshToken });
        
        // Store new access token in localStorage
        localStorage.setItem('token', response.data.access_token);
        
        // Update the original request with the new access token and retry
        originalRequest.headers.Authorization = `Bearer ${response.data.access_token}`;
        return axiosInstance(originalRequest);
      } catch (refreshError) {
        // If refresh token request fails, clear tokens and redirect to login
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');
        window.location.href = '/login';  // Redirect to login
        return Promise.reject(refreshError);
      }
    }

    // If the error is not a 401 or the request is already retried, reject the error
    return Promise.reject(error);
  }
);

export default axiosInstance;


