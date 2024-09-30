// src/components/Home.js
import React from 'react';
import { Typography, Box } from '@mui/material';

const Home = () => {
    return (
        <Box>
            <Typography variant="h2">Welcome to the Patent Management System</Typography>
            <Typography variant="body1">
                This is the home page. Use the navigation to explore the features of the system.
            </Typography>
        </Box>
    );
};

export default Home;
