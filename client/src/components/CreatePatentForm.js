import React, { useState, useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosInstance from '../utils/axiosInstance';
import { UserContext } from '../context/UserContext';

const CreatePatentForm = ({ onPatentCreated }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState('Pending');
  const [users, setUsers] = useState([]);
  const [newUsername, setNewUsername] = useState('');
  const [patentId, setPatentId] = useState(null); 
  const { user } = useContext(UserContext);
  const navigate = useNavigate();

  useEffect(() => {
    if (user?.username && !users.includes(user.username)) {
      setUsers([user.username, ...users]);
    }
  }, [user, users]);

  const handleAddUser = () => {
    if (newUsername && !users.includes(newUsername)) {
      setUsers([...users, newUsername]);
      setNewUsername('');
    }
  };

  const handleRemoveUser = (username) => {
    if (!username) return;
    setUsers(users.filter(user => user !== username));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const createData = {
        title,
        description,
        status,
        users: users 
      };

      const response = await axiosInstance.post('/patents', createData, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });

      const newPatentId = response.data.id; 
      setPatentId(newPatentId); 
      if (newPatentId) {
        onPatentCreated(newPatentId);
        navigate('/dashboard');
      } else {
        console.error('No patent ID received:', newPatentId);
      }
    } catch (error) {
      console.error('Error creating patent', error);
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
      <button type="submit">Create Patent</button>
    </form>
  );
};

export default CreatePatentForm;
