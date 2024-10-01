// src/components/Dashboard.js
import React, { useEffect, useState } from 'react';
import axiosInstance from '../utils/axiosInstance';
import PatentCard from './PatentCard'; // Ensure this path is correct
import CreatePatentForm from './CreatePatentForm'; // Ensure this path is correct

const Dashboard = () => {
  const [stats, setStats] = useState({});
  const [patents, setPatents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await axiosInstance.get('/dashboard');
        setStats(response.data);
      } catch (error) {
        console.error('Error fetching dashboard data', error);
        setError(error);
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
        setError(error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
    fetchPatents();
  }, []);

  const handleDeletePatent = (id) => {
    setPatents(patents.filter(patent => patent.id !== id));
  };

  const handlePatentCreated = (newPatentId) => {
    // Fetch the newly created patent and add it to the state
    axiosInstance.get(`/patents/${newPatentId}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    }).then(response => {
      setPatents([...patents, response.data]);
      // Update the stats
      setStats(prevStats => ({
        ...prevStats,
        patent_count: prevStats.patent_count + 1,
        pending_patents_count: prevStats.pending_patents_count + 1 // Assuming new patents start as pending
      }));
    }).catch(error => {
      console.error('Error fetching new patent', error);
    });
  };

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>Error loading data: {error.message}</p>;
  }

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
      <CreatePatentForm onPatentCreated={handlePatentCreated} />
      <div>
        {patents.length > 0 ? (
          patents.map(patent => (
            <PatentCard key={patent.id} patent={patent} onDelete={handleDeletePatent} />
          ))
        ) : (
          <p>No patents found.</p>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
