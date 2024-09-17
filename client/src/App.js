// src/App.js
import React, { useState } from 'react';
import axios from 'axios';
import jwt_decode from 'jwt-decode';
import { Button, TextField, Container, Typography, Box } from '@mui/material';
import Chat from './components/Chat';
import PatentabilityAnalysis from './components/PatentabilityAnalysis';
import { Line } from 'react-chartjs-2';

function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState('');
  const [user, setUser] = useState(null);

  const register = async () => {
    await axios.post('http://localhost:5000/register', { username, password });
  };

  const login = async () => {
    const response = await axios.post('http://localhost:5000/login', { username, password });
    const token = response.data.access_token;
    setToken(token);
    const decoded = jwt_decode(token);
    setUser(decoded);
  };

  return (
    <Container>
      <Typography variant="h1">Patent Management</Typography>
      <Box>
        <Typography variant="h2">Register</Typography>
        <TextField label="Username" onChange={(e) => setUsername(e.target.value)} />
        <TextField label="Password" type="password" onChange={(e) => setPassword(e.target.value)} />
        <Button variant="contained" onClick={register}>Register</Button>
      </Box>
      <Box>
        <Typography variant="h2">Login</Typography>
        <TextField label="Username" onChange={(e) => setUsername(e.target.value)} />
        <TextField label="Password" type="password" onChange={(e) => setPassword(e.target.value)} />
        <Button variant="contained" onClick={login}>Login</Button>
      </Box>
      {token && (
        <>
          <Chat token={token} />
          <PatentabilityAnalysis token={token} />
          <Box>
            <Typography variant="h2">Patent Analysis Chart</Typography>
            <Line data={{
              labels: ['Novelty', 'Non-obviousness', 'Utility'],
              datasets: [{
                label: 'Patentability Analysis',
                data: [65, 59, 80],
                fill: false,
                backgroundColor: 'rgb(75, 192, 192)',
                borderColor: 'rgba(75, 192, 192, 0.2)',
              }],
            }} />
          </Box>
        </>
      )}
    </Container>
  );
}

export default App;
