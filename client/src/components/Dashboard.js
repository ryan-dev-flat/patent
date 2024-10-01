// src/components/Dashboard.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import PatentCard from './PatentCard'; // Ensure this path is correct
import axiosInstance from '../utils/axiosInstance';

const Dashboard = () => {
  const [stats, setStats] = useState({});
  const [patents, setPatents] = useState([]);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await axiosInstance.get('/dashboard', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        setStats(response.data);
      } catch (error) {
        console.error('Error fetching dashboard data', error);
      }
    };

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

    fetchStats();
    fetchPatents();
  }, []);

  return (
    <div>
      <h2>Patent Summary</h2>
      <p>Total Patents: {stats.patent_count}</p>
      <p>Total Users: {stats.user_count}</p>
      <p>Pending Patents: {stats.pending_patents_count}</p>
      <p>Approved Patents: {stats.approved_patents_count}</p>
      <p>Rejected Patents: {stats.rejected_patents_count}</p>
      <p>Abandoned Patents: {stats.abandoned_patents_count}</p>
      <p>Expired Patents: {stats.expired_patents_count}</p>
      <p>Invalidated Patents: {stats.invalidated_patents_count}</p>
      <div>
        {patents.length > 0 ? (
            patents.map(patent => (
                <PatentCard key={patent.id} patent={patent} />
            ))
        ) : (
            <p>No patents found.</p>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
