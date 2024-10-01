import React, { useState, useEffect } from 'react';
import axiosInstance from '../utils/axiosInstance';

const CreatePatentForm = ({ onPatentCreated }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState('Pending');
  const [users, setUsers] = useState([]);
  const [selectedUsers, setSelectedUsers] = useState([]);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await axiosInstance.get('/users', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        setUsers(response.data);
      } catch (error) {
        console.error('Error fetching users', error);
      }
    };

    fetchUsers();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axiosInstance.post('/patents', {
        title,
        description,
        status,
        user_ids: selectedUsers
      }, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      onPatentCreated(response.data.patent_id);
    } catch (error) {
      console.error('Error creating patent', error);
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
        <select multiple value={selectedUsers} onChange={(e) => setSelectedUsers([...e.target.selectedOptions].map(option => option.value))}>
          {users.map(user => (
            <option key={user.id} value={user.id}>{user.username}</option>
          ))}
        </select>
      </div>
      <button type="submit">Create Patent</button>
    </form>
  );
};

export default CreatePatentForm;
