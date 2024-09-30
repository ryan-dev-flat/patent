import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Container, Typography, Box } from '@mui/material';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './components/Home';
import Register from './components/Register';
import Login from './components/Login';
import Chat from './components/Chat';
import PatentabilityAnalysis from './components/PatentabilityAnalysis';
import Dashboard from './components/Dashboard';
import PatentCards from './components/PatentCards';
import MyChartComponent from './components/MyChartComponent';
import Logout from './components/Logout';

function App() {
  const [token, setToken] = useState('');
  const [user, setUser] = useState(null);

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
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/register" element={<Register setToken={setToken} setUser={setUser} />} />
          <Route path="/login" element={<Login setToken={setToken} setUser={setUser} />} />
          {token && (
            <>
              <Route path="/chat" element={<Chat token={token} />} />
              <Route path="/analysis" element={<PatentabilityAnalysis token={token} />} />
              <Route path="/dashboard" element={<Dashboard token={token} />} />
              <Route path="/patents" element={<PatentCards token={token} />} />
            </>
          )}
        </Routes>
        {token && (
          <Box>
            <Typography variant="h2">Patent Analysis Chart</Typography>
            <MyChartComponent data={chartData} />
            <Logout />
          </Box>
        )}
        <Footer />
      </Container>
    </Router>
  );
}

export default App;
