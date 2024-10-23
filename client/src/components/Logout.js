import React, { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import useAxios from '../utils/useAxios'; // Use useAxios instead of axiosInstance
import { UserContext } from '../context/UserContext';

function Logout() {
  const { logout } = useContext(UserContext); // Access the logout function from UserContext
  const navigate = useNavigate();
  const axiosInstance = useAxios(); // Get the axios instance with token handling

  const handleLogout = async () => {
    try {
      // Call the API to log out (if the backend supports logout endpoint)
      await axiosInstance.post('/logout');

      // Clear the tokens from localStorage
      localStorage.removeItem('token');
      localStorage.removeItem('refreshToken');

      // Update the UserContext to reflect logout (clear user)
      logout();

      // Redirect to login page after successful logout
      navigate('/login');
    } catch (error) {
      console.error('Logout failed', error);

      // Even if the API call fails, ensure the user is logged out locally
      localStorage.removeItem('token');
      localStorage.removeItem('refreshToken');
      logout();
      navigate('/login');
    }
  };

  return (
    <div className="container mt-5">
      <h2>Are you sure you want to logout?</h2>
      <button onClick={handleLogout} className="btn btn-danger">
        Logout
      </button>
    </div>
  );
}

export default Logout;
