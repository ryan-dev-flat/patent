//src/components/dashboard.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Dashboard({ token }) {
    const [patentSummary, setPatentSummary] = useState({});

    useEffect(() => {
        const fetchPatentSummary = async () => {
            try {
                const response = await axios.get('/api/dashboard', {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setPatentSummary(response.data);
            } catch (error) {
                alert('Failed to fetch patent summary');
            }
        };
        fetchPatentSummary();
    }, [token]);

    return (
        <div>
            <h2>Dashboard</h2>
            <div>
                <h3>Total Patents</h3>
                <p>{patentSummary.totalPatents}</p>
                <h3>Pending Patents</h3>
                <p>{patentSummary.pendingPatents}</p>
                <h3>Approved Patents</h3>
                <p>{patentSummary.approvedPatents}</p>
                <h3>Rejected Patents</h3>
                <p>{patentSummary.rejectedPatents}</p>
            </div>
        </div>
    );
}

export default Dashboard;
