// src/components/Dashboard.js
import React, { useEffect, useState } from 'react';
import axiosInstance from '../utils/axiosInstance';
import PatentCard from './PatentCard';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const [patents, setPatents] = useState([]);
  const navigate = useNavigate();

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

  const handleDelete = (id) => {
    setPatents(patents.filter(patent => patent.id !== id));
  };

  const handleUpdate = (id) => {
    navigate(`/patents/${id}/update`);
  };

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      <div className="patent-list">
        {patents.map(patent => (
          <PatentCard key={patent.id} patent={patent} onDelete={handleDelete} onUpdate={handleUpdate} />
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
