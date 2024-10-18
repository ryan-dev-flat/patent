import React, { useState } from 'react';
import axiosInstance from '../utils/axiosInstance';
import { useNavigate } from 'react-router-dom';

const Register = ({ setToken }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(''); 
  const navigate = useNavigate();

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
    <div>
      <h2>Register</h2>
      <form onSubmit={handleRegister}>
        <div>
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Register</button>
      </form>
      {error && <p>{error}</p>}
      {success && <p>{success}</p>}
    </div>
  );
};

export default Register;
