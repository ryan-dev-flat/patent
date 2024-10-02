import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axiosInstance from '../utils/axiosInstance';

const UpdatePatentForm = () => {
  const { patentId } = useParams();
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState('Pending');
  const [users, setUsers] = useState([]);
  const [selectedUsers, setSelectedUsers] = useState([]);
  const [newUsername, setNewUsername] = useState('');
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
        setSelectedUsers(patent.users.map(user => user.id));
      } catch (error) {
        console.error('Error fetching patent', error);
      }
    };

    const fetchUsers = async () => {
      try {
        const response = await axiosInstance.get('/users/all', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        setUsers(response.data);
      } catch (error) {
        console.error('Error fetching users', error);
      }
    };

    fetchPatent();
    fetchUsers();
  }, [patentId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const updateData = {
        title,
        description,
        status,
        user_ids: selectedUsers
      };

      if (newUsername) {
        updateData.username = newUsername;  // Include the new username if provided
      }

      await axiosInstance.patch(`/patents/${patentId}`, updateData, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      navigate('/dashboard'); // Redirect to the dashboard
    } catch (error) {
      console.error('Error updating patent', error);
    }
  };

  const handleAddUser = async () => {
    try {
      await axiosInstance.post(`/patents/${patentId}/add_user`, {
        username: newUsername
      }, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      setNewUsername('');
      // Refresh the list of users associated with the patent
      const response = await axiosInstance.get(`/patents/${patentId}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      setSelectedUsers(response.data.users.map(user => user.id));
    } catch (error) {
      console.error('Error adding user to patent', error);
    }
  };

  const handleRemoveUser = async (userId) => {
    try {
      await axiosInstance.post(`/patents/${patentId}/remove_user`, {
        user_id: userId
      }, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      // Refresh the list of users associated with the patent
      const response = await axiosInstance.get(`/patents/${patentId}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      setSelectedUsers(response.data.users.map(user => user.id));
    } catch (error) {
      console.error('Error removing user from patent', error);
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
        
      </div>
      <div>
        <label>Add User by Username:</label>
        <input type="text" value={newUsername} onChange={(e) => setNewUsername(e.target.value)} />
        <button type="button" onClick={handleAddUser}>Add User</button>
      </div>
      <div>
        <h3>Current Users</h3>
        {Array.isArray(users) && selectedUsers.map(userId => {
          const user = users.find(user => user.id === userId);
          return (
            <div key={userId}>
              <span>{user ? user.username : 'Unknown User'}</span>
              <button type="button" onClick={() => handleRemoveUser(userId)}>Remove</button>
            </div>
          );
        })}
      </div>
      <button type="submit">Update Patent</button>
    </form>
  );
};

export default UpdatePatentForm;
