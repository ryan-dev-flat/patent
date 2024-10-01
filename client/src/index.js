import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import { UserProvider } from './context/UserContext';
import './index.css'; // Assuming you have some global styles

const container = document.getElementById('root');
const root = createRoot(container); // createRoot(container!) if you use TypeScript
root.render(
  <UserProvider>
    <App />
  </UserProvider>
);

