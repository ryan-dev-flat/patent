import React, { useState, useEffect } from 'react';
import useAxios from '../utils/useAxios'; // Use useAxios hook
import { useNavigate } from 'react-router-dom';

const UserAccount = () => {
  const [username, setUsername] = useState('');
  const [newUsername, setNewUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();
  const axiosInstance = useAxios(); // Use Axios instance with token handling

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await axiosInstance.get('/update_user');
        setUsername(response.data.username);
      } catch (error) {
        console.error('Error fetching user data', error);
      }
    };

    fetchUserData();
  }, [axiosInstance]);

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      const updateData = {};
      if (newUsername) updateData.username = newUsername;
      if (password) updateData.password = password;

      const response = await axiosInstance.patch('/update_user', updateData);
      setMessage(response.data.message);
      setNewUsername('');
      setPassword('');
    } catch (error) {
      console.error('Error updating user data', error);
    }
  };

  const handleDelete = async () => {
    try {
      await axiosInstance.delete('/delete_account');
      localStorage.removeItem('token');
      navigate('/register');
    } catch (error) {
      console.error('Error deleting user account', error);
    }
  };

  return (
    <div className="container mt-5">
      <h2>User Account</h2>
      <p>Current Username: <strong>{username}</strong></p>

      {/* Update Form */}
      <form onSubmit={handleUpdate}>
        <div className="mb-3">
          <label htmlFor="newUsername" className="form-label">New Username:</label>
          <input
            type="text"
            id="newUsername"
            className="form-control"
            value={newUsername}
            onChange={(e) => setNewUsername(e.target.value)}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label">New Password:</label>
          <input
            type="password"
            id="password"
            className="form-control"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="submit" className="btn btn-primary">Update</button>
      </form>

      {/* Message */}
      {message && <p className="text-success mt-3">{message}</p>}

      {/* Delete Account Button */}
      <button onClick={handleDelete} className="btn btn-danger mt-3">Delete Account</button>
    </div>
  );
};

export default UserAccount;
