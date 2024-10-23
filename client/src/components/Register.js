import React, { useState } from 'react';
import useAxios from '../utils/useAxios'; // Use useAxios hook
import { useNavigate } from 'react-router-dom';

const Register = ({ setToken }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(''); 
  const navigate = useNavigate();
  const axiosInstance = useAxios(); // Use Axios instance with token handling

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const response = await axiosInstance.post('/register', { username, password });
      console.log('Response:', response); // Log the response
      setToken(response.data.access_token); //  setToken is passed as a prop
      setSuccess('Registration successful! Please log in.');
      setTimeout(() => {
        navigate('/login'); // Redirect to login page after 3 seconds
      }, 3000);
    } catch (error) {
      if (error.response && error.response.data && error.response.data.error ===  'Username already exists') {
        setError('Username already exists. Please choose a different username.');
      } else {
        setError('Registration failed. Please try again.');
      }
      console.error('Error during registration', error);
    }
  };

  return (
    <div className="container mt-5">
      <h2>Register</h2>
      <form onSubmit={handleRegister} className="needs-validation">
        <div className="mb-3">
          <label htmlFor="username" className="form-label">Username:</label>
          <input
            type="text"
            id="username"
            className="form-control"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label">Password:</label>
          <input
            type="password"
            id="password"
            className="form-control"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary">Register</button>
      </form>
      {error && <p className="text-danger mt-3">{error}</p>}
      {success && <p className="text-success mt-3">{success}</p>}
    </div>
  );
};

export default Register;