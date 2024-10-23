// src/utils/useAxios.js
import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { UserContext } from '../context/UserContext';
import axios from 'axios';

// Create the axios instance
const axiosInstance = axios.create({
  baseURL: 'http://localhost:5000/api',
});

const useAxios = () => {
  const { logout } = useContext(UserContext); // Get logout function from UserContext
  const navigate = useNavigate(); // React Router hook to navigate programmatically

  // Variable to prevent multiple refresh token attempts
  let refreshTokenInProgress = false;

  // Axios request interceptor to attach token to headers
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

  // Axios response interceptor to handle 401 errors (token expiration)
  axiosInstance.interceptors.response.use(
    (response) => response,
    async (error) => {
      const originalRequest = error.config;

      // Check if the error is a 401 Unauthorized and it's not a retry
      if (error.response && error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;

        // Attempt to use refresh token
        const refreshToken = localStorage.getItem('refreshToken');
        if (!refreshToken || refreshTokenInProgress) {
          // If no refresh token or a refresh is already in progress, log the user out
          localStorage.removeItem('token');
          localStorage.removeItem('refreshToken');
          logout();
          navigate('/login');
          return Promise.reject(error);
        }

        refreshTokenInProgress = true;  // Prevent multiple refresh attempts

        try {
          // Request a new access token using the refresh token
          const response = await axiosInstance.post('/refresh_token', { token: refreshToken });

          // Save the new access token
          const newAccessToken = response.data.access_token;
          localStorage.setItem('token', newAccessToken);

          // Retry the original request with the new access token
          originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
          refreshTokenInProgress = false;  // Reset the flag after the refresh

          return axiosInstance(originalRequest);  // Retry the request
        } catch (refreshError) {
          // If refresh token fails (e.g., expired), log the user out
          localStorage.removeItem('token');
          localStorage.removeItem('refreshToken');
          logout();
          navigate('/login');
          refreshTokenInProgress = false;  // Reset the flag
          return Promise.reject(refreshError);
        }
      }

      return Promise.reject(error);
    }
  );

  return axiosInstance;
};

export default useAxios;
