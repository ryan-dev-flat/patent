import React from 'react';
import { Link } from 'react-router-dom';
import axiosInstance from '../utils/axiosInstance';

const PatentCard = ({ patent, onDelete }) => {
  const handleDelete = async (id) => {
    try {
      await axiosInstance.delete(`/patents/${id}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      onDelete(id); // Call the callback function to update the parent component's state
    } catch (error) {
      console.error('Error deleting patent', error);
    }
  };

  return (
    <div className="patent-card">
      <h2>{patent.title}</h2>
      <p>{patent.description}</p>
      <p>Status: {patent.status}</p>
      {/* Uncomment and adjust if you want to display other users */}
      {/* <p>Other Users: {patent.user.map(u => u.username).join(', ')}</p> */}
      <p>Utility Score: {patent.utility?.score || 'N/A'}</p>
      <p>Novelty Score: {patent.novelty?.score || 'N/A'}</p>
      <p>Obviousness Score: {patent.obviousness?.score || 'N/A'}</p>
      <p>Patentability Score: {patent.patentability_score || 'N/A'}</p>
      <button onClick={() => handleDelete(patent.id)}>Delete</button>
      <Link to={`/patents/${patent.id}/update`}>Update</Link>
      <Link to={`/patents/${patent.id}/prior_art`}>Show Prior Art</Link>
      <Link to={`/patents/${patent.id}/analysis`}>Analyze</Link>
      <Link to={`/patents/${patent.id}/chart`}>View Chart</Link>
    </div>
  );
};

export default PatentCard;

