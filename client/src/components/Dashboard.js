import React, { useEffect, useState } from 'react';
import useAxios from '../utils/useAxios'; // Use useAxios hook for Axios instance
import PatentCard from './PatentCard'; 
import CreatePatentForm from './CreatePatentForm'; 

const Dashboard = () => {
    const [stats, setStats] = useState({});
    const [patents, setPatents] = useState([]);
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const axiosInstance = useAxios(); // Get Axios instance with token handling

    // Fetch dashboard statistics
    const fetchStats = async () => {
        try {
            const response = await axiosInstance.get('/dashboard');
            setStats(response.data);
        } catch (error) {
            console.error('Error fetching dashboard data', error);
            setError(error);
        }
    };

    // Fetch all patents
    const fetchPatents = async () => {
        try {
            const response = await axiosInstance.get('/patents');
            setPatents(response.data);
        } catch (error) {
            console.error('Error fetching patents', error);
            setError(error);
        } finally {
            setLoading(false);
        }
    };

    // Fetch all users
    const fetchUsers = async () => {
        try {
            const response = await axiosInstance.get('/users/all');
            setUsers(response.data);
        } catch (error) {
            console.error('Error fetching users', error);
            setError(error);
        }
    };

    useEffect(() => {
        fetchStats();
        fetchPatents();
        fetchUsers();
    }, [axiosInstance]);

    // Handle patent deletion
    const handleDeletePatent = (id) => {
        setPatents(patents.filter(patent => patent.id !== id));
        // Update the stats accordingly
        setStats(prevStats => ({
            ...prevStats,
            patent_count: prevStats.patent_count - 1,
            pending_patents_count: prevStats.pending_patents_count - 1 // Adjust based on the patent's status
        }));
    };

    // Handle patent creation
    const handlePatentCreated = async (newPatentId) => {
        if (!newPatentId) {
            console.error('No patent ID received:', newPatentId);
            return;
        }
        // Fetch the newly created patent and add it to the state
        try {
            const response = await axiosInstance.get(`/patents/${newPatentId}`);
            setPatents([response.data, ...patents]); // Prepend the new patent
            // Update the stats
            setStats(prevStats => ({
                ...prevStats,
                patent_count: prevStats.patent_count + 1,
                pending_patents_count: prevStats.pending_patents_count + 1 // Assuming new patents start as pending
            }));
        } catch (error) {
            console.error('Error fetching new patent:', error);
        }
    };

    // Handle patent update
    const handlePatentUpdated = async (updatedPatentId) => {
        try {
          // Fetch the updated patent
          const response = await axiosInstance.get(`/patents/${updatedPatentId}`);
          const updatedPatent = response.data;
      
          // Log the updated patent data received from the server
          console.log('Updated patent fetched from server:', updatedPatent);
      
          // Log the current state of patents before updating
          console.log('Current patents state:', patents);
      
          // Update the state with the newly fetched patent data
          setPatents((prevPatents) =>
            prevPatents.map((patent) =>
              patent.id === updatedPatentId ? updatedPatent : patent
            )
          );
      
          // Log the state after updating patents
          console.log('Updated patents state:', patents);
        } catch (error) {
          console.error('Error fetching updated patent', error);
        }
      };
      
      

    if (loading) {
        return <p>Loading...</p>;
    }

    if (error) {
        return <p>Error loading data: {error.message}</p>;
    }

    return (
        <div className="container mt-5">
          <h2>Dashboard</h2>
          <div className="row">
            <div className="col-md-4">
              <div className="card">
                <div className="card-body">
                  <h5 className="card-title">Patent Summary</h5>
                  <p>Total Patents: {stats.patent_count}</p>
                  <p>Total Users: {stats.user_count}</p>
                  <p>Pending Patents: {stats.pending_patents_count}</p>
                  <p>Approved Patents: {stats.approved_patents_count}</p>
                </div>
              </div>
            </div>
    
            <div className="col-md-8">
              <CreatePatentForm />
              <div className="row mt-3">
                {patents.length > 0 ? (
                  patents.map(patent => (
                    <div className="col-md-6 mb-3" key={patent.id}>
                      <PatentCard patent={patent} />
                    </div>
                  ))
                ) : (
                  <p>No patents found.</p>
                )}
              </div>
            </div>
          </div>
        </div>
      );
    };
    
    export default Dashboard;