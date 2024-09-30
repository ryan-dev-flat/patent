// src/components/Dashboard.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import PatentCard from './PatentCard';

function Dashboard({ token, setToken, setUser }) {
    const [patents, setPatents] = useState([]);
    const [newPatent, setNewPatent] = useState({ title: '', description: '' });

    useEffect(() => {
        const fetchPatents = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/patents', {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setPatents(response.data);
            } catch (error) {
                alert('Failed to fetch patents');
            }
        };
        fetchPatents();
    }, [token]);

    const handleCreatePatent = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:5000/api/patents', newPatent, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setPatents([...patents, response.data]);
            setNewPatent({ title: '', description: '' });
        } catch (error) {
            alert('Failed to create patent');
        }
    };

    const handleDeleteAccount = async () => {
        try {
            await axios.delete('http://127.0.0.1:5000/api/delete_account', {
                headers: { Authorization: `Bearer ${token}` }
            });
            setToken('');
            setUser(null);
            alert('Account deleted successfully');
        } catch (error) {
            alert('Failed to delete account');
        }
    };

    return (
        <div>
            <h2>Dashboard</h2>
            <div>
                <h3>Create New Patent</h3>
                <input
                    type="text"
                    placeholder="Title"
                    value={newPatent.title}
                    onChange={(e) => setNewPatent({ ...newPatent, title: e.target.value })}
                />
                <textarea
                    placeholder="Description"
                    value={newPatent.description}
                    onChange={(e) => setNewPatent({ ...newPatent, description: e.target.value })}
                />
                <button onClick={handleCreatePatent}>Create Patent</button>
            </div>
            <div>
                <h3>Your Patents</h3>
                {patents.map((patent) => (
                    <PatentCard key={patent.id} patent={patent} token={token} setPatents={setPatents} />
                ))}
            </div>
            <button onClick={handleDeleteAccount}>Delete Account</button>
        </div>
    );
}

export default Dashboard;
