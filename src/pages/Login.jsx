import React, { useState } from 'react';
import Input from '../components/Input';
import Button from '../components/Button';
import Alert from '../components/Alert';
import Card from '../components/Card';
import { login, savePasswordTemporarily } from '../services/authService';

/**
 * Login Page
 */
const Login = ({ onLogin }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [errors, setErrors] = useState({});
  const [alert, setAlert] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    setLoading(true);
    try {
      const result = login({
        email: formData.email,
        password: formData.password
      });

      if (result.success) {
        // Save password temporarily (MVP only)
        savePasswordTemporarily(result.user.id, formData.password);

        setAlert({
          type: 'success',
          title: 'Welcome Back!',
          message: 'You have successfully signed in. Redirecting to dashboard...'
        });

        setTimeout(() => {
          onLogin(result.user);
          window.location.href = '/dashboard';
        }, 2000);
      } else {
        setAlert({
          type: 'danger',
          title: 'Sign In Failed',
          message: result.error
        });
      }
    } catch (error) {
      setAlert({
        type: 'danger',
        title: 'Error',
        message: 'An unexpected error occurred. Please try again.'
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '500px', margin: '0 auto', padding: 'var(--space-lg)' }}>
      <Card title="Sign In" subtitle="Welcome back to SecureShare">
        {alert && (
          <Alert
            type={alert.type}
            title={alert.title}
            message={alert.message}
            onClose={() => setAlert(null)}
          />
        )}

        <form onSubmit={handleSubmit}>
          <Input
            label="Email Address"
            type="email"
            name="email"
            value={formData.email}
            onChange={handleInputChange}
            placeholder="you@example.com"
            required
            error={errors.email}
          />

          <Input
            label="Password"
            type="password"
            name="password"
            value={formData.password}
            onChange={handleInputChange}
            placeholder="••••••••"
            required
            error={errors.password}
          />

          <Button
            type="submit"
            variant="primary"
            fullWidth
            loading={loading}
            disabled={loading}
          >
            {loading ? 'Signing In...' : 'Sign In'}
          </Button>
        </form>

        <p style={{ marginTop: 'var(--space-lg)', textAlign: 'center' }}>
          Don't have an account?{' '}
          <a href="/signup" style={{ color: 'var(--color-primary)', fontWeight: 'var(--font-weight-semibold)' }}>
            Sign Up
          </a>
        </p>

        <div style={{ marginTop: 'var(--space-lg)', padding: 'var(--space-md)', background: 'var(--color-bg-secondary)', borderRadius: 'var(--radius-md)' }}>
          <p className="text-small" style={{ marginBottom: 'var(--space-sm)' }}>
            <strong>Demo Account (MVP Testing):</strong>
          </p>
          <p className="text-small">Email: demo@test.com</p>
          <p className="text-small">Password: demo123</p>
        </div>
      </Card>
    </div>
  );
};

export default Login;
