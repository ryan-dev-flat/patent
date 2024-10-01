import React, { useEffect, useState } from 'react';

import { Link } from 'react-router-dom';
import axiosInstance from '../utils/axiosInstance';


const PatentCard = () => {
  const [patents, setPatents] = useState([]);

  useEffect(() => {
    const fetchPatents = async () => {
      try {
        const response = await axiosInstance.get('/patents', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        setPatents(response.data);
      } catch (error) {
        console.error('Error fetching patents', error);
      }
    };

    fetchPatents();
  }, []);

  const handleDelete = async (id) => {
    try {
      await axiosInstance.delete(`/patents/${id}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      setPatents(patents.filter(patent => patent.id !== id));
    } catch (error) {
      console.error('Error deleting patent', error);
    }
  };

  return (
    <div>
      <h1>Patents</h1>
      {patents.map(patent => (
        <div key={patent.id} className="patent-card">
          <h2>{patent.title}</h2>
          <p>{patent.description}</p>
          <p>Status: {patent.status}</p>
          <p>Other Users: {patent.user.map(u => u.username).join(', ')}</p>
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
      ))}
    </div>
  );
};

export default PatentCard;
