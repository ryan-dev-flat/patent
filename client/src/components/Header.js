// src/components/Header.js
import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { UserContext } from '../context/UserContext';

const Header = () => {
  const { user } = useContext(UserContext);

  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
      <div className="container-fluid">
        <Link className="navbar-brand" to="/">Patent Management</Link>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse" // Updated attribute
          data-bs-target="#navbarNav" // Updated attribute
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav">
            {user ? (
              <>
                {/* Show these links only when the user is logged in */}
                <li className="nav-item">
                  <Link className="nav-link" to="/dashboard">Dashboard</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/create-patent">Create Patent</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/user-account">User Account</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/logout">Logout</Link>
                </li>
              </>
            ) : (
              <>
                {/* Show only Login and Register links when the user is not logged in */}
                <li className="nav-item">
                  <Link className="nav-link" to="/login">Login</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/register">Register</Link>
                </li>
              </>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Header;
