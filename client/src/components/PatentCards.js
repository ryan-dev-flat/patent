import React, { useState, useEffect } from 'react';
import axios from 'axios';

function PatentCards({ token }) {
    const [patents, setPatents] = useState([]);
    const [selectedPatent, setSelectedPatent] = useState(null);

    useEffect(() => {
        const fetchPatents = async () => {
            try {
                const response = await axios.get('/api/patents', {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setPatents(response.data);
            } catch (error) {
                alert('Failed to fetch patents');
            }
        };
        fetchPatents();
    }, [token]);

    const handleUpdatePatent = async (patentId, updatedPatent) => {
        try {
            await axios.patch(`/api/patents/${patentId}`, updatedPatent, {
                headers: { Authorization: `Bearer ${token}` }
            });
            alert('Patent updated successfully');
            // Refresh the patents list
            const response = await axios.get('/api/patents', {
                headers: { Authorization: `Bearer ${token}` }
            });
            setPatents(response.data);
        } catch (error) {
            alert('Failed to update patent');
        }
    };

    const handleDeletePatent = async (patentId) => {
        try {
            await axios.delete(`/api/patents/${patentId}`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            alert('Patent deleted successfully');
            // Refresh the patents list
            const response = await axios.get('/api/patents', {
                headers: { Authorization: `Bearer ${token}` }
            });
            setPatents(response.data);
        } catch (error) {
            alert('Failed to delete patent');
        }
    };

    return (
        <div>
            <h2>Patent Cards</h2>
            <div>
                {patents.map((patent, index) => (
                    <div key={index} className="patent-card">
                        <h3>{patent.title}</h3>
                        <p>{patent.description}</p>
                        <button onClick={() => setSelectedPatent(patent)}>View Details</button>
                        <button onClick={() => handleUpdatePatent(patent.id, { title: patent.title, description: patent.description })}>Update</button>
                        <button onClick={() => handleDeletePatent(patent.id)}>Delete</button>
                        <button onClick={() => alert('Patentability Analysis')}>Patentability Analysis</button>
                    </div>
                ))}
            </div>
            {selectedPatent && (
                <div className="patent-details">
                    <h3>Patent Details</h3>
                    <p>Title: {selectedPatent.title}</p>
                    <p>Description: {selectedPatent.description}</p>
                    {/* Add more details as needed */}
                </div>
            )}
        </div>
    );
}

export default PatentCards;
