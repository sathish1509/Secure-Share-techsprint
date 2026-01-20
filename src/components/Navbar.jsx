import React from 'react';

/**
 * Navigation Bar Component
 * Displays the app logo, main menu, and user actions
 */
const Navbar = ({ user, onLogout }) => {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <span>🔐</span>
          <span>SecureShare</span>
        </div>

        <div className="navbar-menu">
          <a href="/" className="navbar-link">
            Home
          </a>
          {user ? (
            <>
              <a href="/dashboard" className="navbar-link">
                Dashboard
              </a>
              <a href="/upload" className="navbar-link">
                Upload
              </a>
              <a href="/my-files" className="navbar-link">
                My Files
              </a>
              <div className="flex gap-md" style={{ alignItems: 'center' }}>
                <span className="text-small" style={{ color: 'var(--color-text-secondary)' }}>
                  {user.name}
                </span>
                <button className="btn btn-secondary btn-small" onClick={onLogout}>
                  Logout
                </button>
              </div>
            </>
          ) : (
            <>
              <a href="/login" className="navbar-button">
                Login
              </a>
              <a href="/signup" className="navbar-button">
                Sign Up
              </a>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
