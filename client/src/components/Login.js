//./src/components/Login.js
import React, { useState } from 'react';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

function Login({ setToken, setUser }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleLogin = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:5000/api/login', { username, password });
            const token = response.data.access_token;
            localStorage.setItem('token', token);
            const decoded = jwtDecode(token);
            setToken(token);
            setUser(decoded);
            alert('Login successful');
        } catch (error) {
            alert('Login failed');
        }
    };

    return (
        <div>
            <h2>Login</h2>
            <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
            <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
            <button onClick={handleLogin}>Login</button>
        </div>
    );
}

export default Login;
