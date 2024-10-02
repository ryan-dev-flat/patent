import React, { useState, useEffect } from 'react';
import axiosInstance from '../utils/axiosInstance';
import { useNavigate } from 'react-router-dom';

const UserAccount = () => {
  const [username, setUsername] = useState('');
  const [newUsername, setNewUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await axiosInstance.get('/update_user', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        setUsername(response.data.username);
      } catch (error) {
        console.error('Error fetching user data', error);
      }
    };

    fetchUserData();
  }, []);

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      const updateData = {};
      if (newUsername) updateData.username = newUsername;
      if (password) updateData.password = password;

      const response = await axiosInstance.patch('/update_user', updateData, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      setMessage(response.data.message);
      setNewUsername('');
      setPassword('');
    } catch (error) {
      console.error('Error updating user data', error);
    }
  };

  const handleDelete = async () => {
    try {
      await axiosInstance.delete('/delete_account', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      localStorage.removeItem('token');
      navigate('/register');
    } catch (error) {
      console.error('Error deleting user account', error);
    }
  };

  return (
    <div>
      <h2>User Account</h2>
      <p>Current Username: {username}</p>
      <form onSubmit={handleUpdate}>
        <div>
          <label>New Username:</label>
          <input
            type="text"
            value={newUsername}
            onChange={(e) => setNewUsername(e.target.value)}
          />
        </div>
        <div>
          <label>New Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="submit">Update</button>
      </form>
      {message && <p>{message}</p>}
      <button onClick={handleDelete}>Delete Account</button>
    </div>
  );
};

export default UserAccount;
