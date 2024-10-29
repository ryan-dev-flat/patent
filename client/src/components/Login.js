import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import useAxios from '../utils/useAxios'; // Use the custom Axios hook
import { UserContext } from '../context/UserContext';
import {jwtDecode} from 'jwt-decode'; // Correct import for jwtDecode

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { login } = useContext(UserContext); // Get login function from UserContext

  const axiosInstance = useAxios(); // Get Axios instance with the token handling logic

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      // Make the API request to the login endpoint
      const response = await axiosInstance.post('/login', { username, password });
      
      // Assuming the response includes both access and refresh tokens
      const accessToken = response.data.access_token;
      const refreshToken = response.data.refresh_token; // If provided by the backend
      
      // Store tokens in localStorage
      localStorage.setItem('token', accessToken);
      if (refreshToken) {
        localStorage.setItem('refreshToken', refreshToken);
      }

      // Decode the access token to get user details
      const decodedUser = jwtDecode(accessToken);
      
      // Update user context
      login(decodedUser, accessToken);

      // Redirect to the dashboard on successful login
      alert('Login successful');
      navigate('/dashboard');
    } catch (error) {
      console.error('Login error:', error);
      setError('Login failed. Please check your username and password.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5">
      <h2>Login</h2>
      <form onSubmit={handleLogin} className="needs-validation">
        <div className="mb-3">
          <input
            type="text"
            placeholder="Username"
            className="form-control"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <input
            type="password"
            placeholder="Password"
            className="form-control"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
      {error && <p className="text-danger mt-3">{error}</p>}
    </div>
  );
}

export default Login;
