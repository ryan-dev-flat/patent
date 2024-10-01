import React, { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { UserContext } from '../context/UserContext';
import axiosInstance from '../utils/axiosInstance';

function Logout() {
  const { logout } = useContext(UserContext);
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await axiosInstance.post('/logout'); // Assuming you have a logout endpoint
      logout();
      navigate('/login');
    } catch (error) {
      console.error('Logout failed', error);
    }
  };

  return (
    <button onClick={handleLogout}>
      Logout
    </button>
  );
}

export default Logout;

