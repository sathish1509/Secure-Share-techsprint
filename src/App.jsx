import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Landing from './pages/Landing';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import FileUpload from './pages/FileUpload';
import MyFiles from './pages/MyFiles';
import { logout } from './services/authService';
import { getUserProfile } from './services/storageService';
import './styles/globals.css';
import './styles/components.css';

/**
 * App Component - Main application entry point
 * Handles routing, authentication state, and layout
 */
function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Check for existing user session on mount
  useEffect(() => {
    const currentUser = getUserProfile();
    if (currentUser) {
      setUser(currentUser);
    }
    setLoading(false);
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleSignup = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    logout();
    setUser(null);
    window.location.href = '/';
  };

  // Protected route wrapper
  const ProtectedRoute = ({ children }) => {
    if (loading) {
      return (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100vh',
          background: 'var(--color-bg-secondary)'
        }}>
          <div style={{ textAlign: 'center' }}>
            <div className="spinner" style={{
              width: '40px',
              height: '40px',
              margin: '0 auto var(--space-lg)',
              borderWidth: '4px'
            }}></div>
            <p>Loading...</p>
          </div>
        </div>
      );
    }

    if (!user) {
      return <Navigate to="/login" replace />;
    }

    return children;
  };

  if (loading) {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        background: 'var(--color-bg-secondary)'
      }}>
        <div style={{ textAlign: 'center' }}>
          <div className="spinner" style={{
            width: '40px',
            height: '40px',
            margin: '0 auto var(--space-lg)',
            borderWidth: '4px'
          }}></div>
          <p>Loading SecureShare...</p>
        </div>
      </div>
    );
  }

  return (
    <Router>
      <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        <Navbar user={user} onLogout={handleLogout} />

        <main style={{ flex: 1, paddingBottom: 'var(--space-2xl)' }}>
          <Routes>
            {/* Public Routes */}
            <Route path="/" element={<Landing user={user} />} />
            <Route path="/login" element={!user ? <Login onLogin={handleLogin} /> : <Navigate to="/dashboard" replace />} />
            <Route path="/signup" element={!user ? <Signup onSignup={handleSignup} /> : <Navigate to="/dashboard" replace />} />

            {/* Protected Routes */}
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <Dashboard user={user} />
                </ProtectedRoute>
              }
            />
            <Route
              path="/upload"
              element={
                <ProtectedRoute>
                  <FileUpload />
                </ProtectedRoute>
              }
            />
            <Route
              path="/my-files"
              element={
                <ProtectedRoute>
                  <MyFiles />
                </ProtectedRoute>
              }
            />

            {/* Catch-all */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>

        <Footer />
      </div>
    </Router>
  );
}

export default App;
