import React, { useState, useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosInstance from '../utils/useAxios';
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

      const response = await axiosInstance.post('/patents', createData);
      console.log('Response data:', response.data); 
      const newPatentId = response.data.patent_id; 
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
    <div className="container mt-5">
      <h2>Create New Patent</h2>
      <form onSubmit={handleSubmit}>
        {/* Title */}
        <div className="mb-3">
          <label htmlFor="title" className="form-label">Title</label>
          <input
            type="text"
            id="title"
            className="form-control"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </div>

        {/* Description */}
        <div className="mb-3">
          <label htmlFor="description" className="form-label">Description</label>
          <textarea
            id="description"
            className="form-control"
            rows="3"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          ></textarea>
        </div>

        {/* Status */}
        <div className="mb-3">
          <label htmlFor="status" className="form-label">Status</label>
          <select
            id="status"
            className="form-select"
            value={status}
            onChange={(e) => setStatus(e.target.value)}
            required
          >
            <option value="Pending">Pending</option>
            <option value="Granted">Granted</option>
            <option value="Rejected">Rejected</option>
            <option value="Expired">Expired</option>
            <option value="Abandoned">Abandoned</option>
          </select>
        </div>

        {/* Add Users */}
        <div className="mb-3">
          <label htmlFor="newUser" className="form-label">Add Additional Users</label>
          <div className="input-group mb-3">
            <input
              type="text"
              id="newUser"
              className="form-control"
              value={newUsername}
              onChange={(e) => setNewUsername(e.target.value)}
            />
            <button
              type="button"
              className="btn btn-primary"
              onClick={handleAddUser}
            >
              Add User
            </button>
          </div>
          <ul className="list-group">
            {users.map((username, index) => (
              <li key={index} className="list-group-item d-flex justify-content-between align-items-center">
                {username}
                {username !== user?.username && (
                  <button
                    type="button"
                    className="btn btn-danger btn-sm"
                    onClick={() => handleRemoveUser(username)}
                  >
                    Remove
                  </button>
                )}
              </li>
            ))}
          </ul>
        </div>

        {/* Submit Button */}
        <button type="submit" className="btn btn-success">Create Patent</button>
      </form>
    </div>
  );
};

export default CreatePatentForm;