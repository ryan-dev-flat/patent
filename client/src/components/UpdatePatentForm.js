import React, { useState, useEffect, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import useAxios from '../utils/useAxios';
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
  const axiosInstance = useAxios(); // Use Axios instance with token handling

  useEffect(() => {
    const fetchPatent = async () => {
      try {
        const response = await axiosInstance.get(`/patents/${patentId}`);
        const patent = response.data;
        console.log(response.data);
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
        await axiosInstance.post(`/patents/${patentId}/add_user`, { username: newUsername });
  
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
      await axiosInstance.post(`/patents/${patentId}/remove_user`, { username });
      setUsers(users.filter(user => user !== username)); // Update local state
      console.log('Removing User:', { user: username });
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
  
      // Log the data you're sending to the backend
      console.log('Submitting update data:', updateData);
  
      const response = await axiosInstance.patch(`/patents/${patentId}`, updateData);
  
      if (response.data) {
        // Log the response from the server after the update
        console.log('Response after update:', response.data);
  
        // Fetch the updated patent and log the response
        const updatedPatentResponse = await axiosInstance.get(`/patents/${patentId}`);
        console.log('Updated patent data:', updatedPatentResponse.data);
  
        onPatentUpdated(updatedPatentResponse.data.id);
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
    <div className="container mt-5">
      <h2>Update Patent</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="title" className="form-label">Title</label>
          <input
            type="text"
            className="form-control"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </div>

        <div className="mb-3">
          <label htmlFor="description" className="form-label">Description</label>
          <textarea
            className="form-control"
            id="description"
            rows="3"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          ></textarea>
        </div>

        <div className="mb-3">
          <label htmlFor="status" className="form-label">Status</label>
          <select
            className="form-select"
            id="status"
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

        <div className="mb-3">
          <label htmlFor="newUser" className="form-label">Add User</label>
          <input
            type="text"
            className="form-control"
            id="newUser"
            value={newUsername}
            onChange={(e) => setNewUsername(e.target.value)}
          />
          <button type="button" className="btn btn-primary mt-2" onClick={handleAddUser}>Add User</button>
          <ul className="list-group mt-3">
            {users.map((username, index) => (
              <li key={index} className="list-group-item">
                {username}
                {username !== user?.username && (
                  <button
                    type="button"
                    className="btn btn-danger btn-sm float-end"
                    onClick={() => setUsers(users.filter(u => u !== username))}
                  >
                    Remove
                  </button>
                )}
              </li>
            ))}
          </ul>
        </div>

        <button type="submit" className="btn btn-success">Update Patent</button>
      </form>
    </div>
  );
};

export default UpdatePatentForm;