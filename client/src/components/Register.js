//src/components/Register.js
import React, { useState } from 'react';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

function Register({ setToken, setUser }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleRegister = async () => {
        try {
            const response = await axios.post('http://localhost:5000/api/register', { username, password });
            console.log('Response:', response);  // Log the response
            if (response.status === 201) {
                const token = response.data.access_token;
                localStorage.setItem('token', token);
                const decoded = jwtDecode(token);
                setToken(token);
                setUser(decoded);
                alert('Registration successful');
            } else {
                alert('Registration failed');
            }
        } catch (error) {
            console.error('Error:', error);  // Log the error
            if (error.response && error.response.data.error) {
                alert(error.response.data.error);
            } else {
                alert('Registration failed');
            }
        }
    };

    return (
        <div>
            <h2>Register</h2>
            <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
            <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
            <button onClick={handleRegister}>Register</button>
        </div>
    );
}

export default Register;
