import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import { UserProvider } from './context/UserContext';
import './index.css'; 
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';


const container = document.getElementById('root');
const root = createRoot(container); 
root.render(
  <UserProvider>
    <App />
  </UserProvider>
);

