import React, { useState } from 'react';
import axios from 'axios';
import jwtDecode from 'jwt-decode';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Button, TextField, Container, Typography, Box } from '@mui/material';
import Chat from './components/Chat';
import PatentabilityAnalysis from './components/PatentabilityAnalysis';
import Dashboard from './components/Dashboard';
import PatentCards from './components/PatentCards';
import Header from './components/Header';
import Footer from './components/Footer';
import MyChartComponent from './components/MyChartComponent';
import Logout from './components/Logout';  // Import the Logout component
import Home from './components/Home';
import Login from './components/Login';

function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState('');
  const [user, setUser] = useState(null);

  const register = async () => {
    await axios.post('http://localhost:5000/api/register', { username, password });
  };

  const login = async () => {
    try {
        const response = await axios.post('http://localhost:5000/api/login', { username, password });
        const token = response.data.access_token;
        console.log('Token:', token);  // Log the token
        const decoded = jwtDecode(token);
        console.log('Decoded:', decoded);  // Log the decoded token
        setToken(token);
        setUser(decoded);
    } catch (error) {
        console.error('Login failed', error);
    }
};


  const chartData = {
    labels: ['Novelty', 'Non-obviousness', 'Utility'],
    datasets: [{
      label: 'Patentability Analysis',
      data: [65, 59, 80],
      fill: false,
      backgroundColor: 'rgb(75, 192, 192)',
      borderColor: 'rgba(75, 192, 192, 0.2)',
    }],
  };

  return (
    <Router>
      <Container>
        <Header />
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
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/chat" element={<Chat token={token} />} />
              <Route path="/analysis" element={<PatentabilityAnalysis token={token} />} />
              <Route path="/dashboard" element={<Dashboard token={token} />} />
              <Route path="/patents" element={<PatentCards token={token} />} />
            </Routes>
            <Box>
              <Typography variant="h2">Patent Analysis Chart</Typography>
              <MyChartComponent data={chartData} />
            </Box>
            <Logout />  {/* Add the Logout component */}
          </>
        )}
        <Footer />
      </Container>
    </Router>
  );
}

export default App;
