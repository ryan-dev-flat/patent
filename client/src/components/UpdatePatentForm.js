import React, { useState, useEffect, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axiosInstance from '../utils/axiosInstance';
import { UserContext } from '../context/UserContext';

const UpdatePatentForm = ({ onPatentUpdated = () => {} }) => {
  const { patentId } = useParams(); // Get patentId from URL params
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState('Pending');
  const [users, setUsers] = useState([]);
  const [newUsername, setNewUsername] = useState('');
  const [error, setError] = useState(null);
  const { user } = useContext(UserContext);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPatent = async () => {
      try {
        const response = await axiosInstance.get(`/patents/${patentId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        const patent = response.data;
        setTitle(patent.title);
        setDescription(patent.description);
        setStatus(patent.status);
        setUsers(patent.users.map(user => user.username));
      } catch (error) {
        console.error('Error fetching patent:', error);
      }
    };

    fetchPatent();
  }, [patentId]);

  const handleAddUser = async () => {
    if (newUsername && !users.includes(newUsername)) {
      try {
        // Send the username directly to the backend
        await axiosInstance.post(`/patents/${patentId}/add_user`, { username: newUsername }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
  
        setUsers([...users, newUsername]);
        setNewUsername('');
        console.log('Sending data:', { username: newUsername });
      } catch (err) {
        console.error('Error adding user to patent', err);
        setError('Failed to add user to patent');
      }
    }
  };
  
  

  const handleRemoveUser = async (username) => {
    try {
      // Make API call to remove user from the patent
      await axiosInstance.post(`/patents/${patentId}/remove_user`, { username }, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      setUsers(users.filter(user => user !== username)); // Update local state
    } catch (err) {
      console.error('Error removing user from patent', err);
      setError('Failed to remove user from patent');
    }
  };
  

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const updateData = {
        title,
        description,
        status,
        users: users
      };

      const response = await axiosInstance.patch(`/patents/${patentId}`, updateData, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (response.data) {
        onPatentUpdated(patentId);
        navigate('/dashboard');
      } else {
        console.error('Error updating patent:', response.data);
      }
    } catch (error) {
      console.error('Error updating patent:', error);
      if (error.response) {
        console.error('Response data:', error.response.data);
      }
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Title:</label>
        <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} required />
      </div>
      <div>
        <label>Description:</label>
        <textarea value={description} onChange={(e) => setDescription(e.target.value)} required></textarea>
      </div>
      <div>
        <label>Status:</label>
        <select value={status} onChange={(e) => setStatus(e.target.value)} required>
          <option value="Pending">Pending</option>
          <option value="Granted">Granted</option>
          <option value="Rejected">Rejected</option>
          <option value="Expired">Expired</option>
          <option value="Abandoned">Abandoned</option>
        </select>
      </div>
      <div>
        <label>Additional Users:</label>
        <input
          type="text"
          value={newUsername}
          onChange={(e) => setNewUsername(e.target.value)}
        />
        <button type="button" onClick={handleAddUser}>Add User</button>
        <ul>
          {users.map((username, index) => (
            <li key={index}>
              {username}
              {username !== user?.username && (
                <button type="button" onClick={() => handleRemoveUser(username)}>Remove</button>
              )}
            </li>
          ))}
        </ul>
      </div>
      <button type="submit">Update Patent</button>
    </form>
  );
};

export default UpdatePatentForm;
