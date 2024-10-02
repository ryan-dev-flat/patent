import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosInstance from '../utils/axiosInstance';
import { UserContext } from '../context/UserContext';

const CreatePatentForm = ({ onPatentCreated }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState('Pending');
  const [inventors, setInventors] = useState([]);
  const [newUsername, setNewUsername] = useState('');
  const navigate = useNavigate();
  const { user } = useContext(UserContext);

  const handleAddInventor = () => {
    if (newUsername && !inventors.includes(newUsername)) {
      setInventors([...inventors, newUsername]);
      setNewUsername('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const createData = {
        title,
        description,
        status,
        inventors: [user.username, ...inventors]
      };

      const response = await axiosInstance.post('/patents', createData, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      onPatentCreated(response.data.patent_id);
      navigate('/dashboard'); // Redirect to the dashboard
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
        <label>Additional Inventors:</label>
        <input
          type="text"
          value={newUsername}
          onChange={(e) => setNewUsername(e.target.value)}
        />
        <button type="button" onClick={handleAddInventor}>Add Inventor</button>
        <ul>
          <li>{user.username} (Current User)</li>
          {inventors.map((inventor, index) => (
            <li key={index}>{inventor}</li>
          ))}
        </ul>
      </div>
      <button type="submit">Create Patent</button>
    </form>
  );
};

export default CreatePatentForm;

