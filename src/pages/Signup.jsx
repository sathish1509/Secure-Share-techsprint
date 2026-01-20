import React, { useState } from 'react';
import Input from '../components/Input';
import Button from '../components/Button';
import Alert from '../components/Alert';
import Card from '../components/Card';
import { signup, savePasswordTemporarily } from '../services/authService';

/**
 * Sign Up Page
 */
const Signup = ({ onSignup }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
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

    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Invalid email format';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    setLoading(true);
    try {
      const result = signup({
        email: formData.email,
        password: formData.password,
        name: formData.name
      });

      if (result.success) {
        // Save password temporarily (MVP only - do NOT do this in production!)
        savePasswordTemporarily(result.user.id, formData.password);

        setAlert({
          type: 'success',
          title: 'Account Created!',
          message: 'You have successfully signed up. Redirecting to dashboard...'
        });

        setTimeout(() => {
          onSignup(result.user);
          window.location.href = '/dashboard';
        }, 2000);
      } else {
        setAlert({
          type: 'danger',
          title: 'Sign Up Failed',
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
      <Card title="Create Your Account" subtitle="Join SecureShare and secure your files">
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
            label="Full Name"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
            placeholder="John Doe"
            required
            error={errors.name}
          />

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

          <Input
            label="Confirm Password"
            type="password"
            name="confirmPassword"
            value={formData.confirmPassword}
            onChange={handleInputChange}
            placeholder="••••••••"
            required
            error={errors.confirmPassword}
          />

          <Button
            type="submit"
            variant="primary"
            fullWidth
            loading={loading}
            disabled={loading}
          >
            {loading ? 'Creating Account...' : 'Sign Up'}
          </Button>
        </form>

        <p style={{ marginTop: 'var(--space-lg)', textAlign: 'center' }}>
          Already have an account?{' '}
          <a href="/login" style={{ color: 'var(--color-primary)', fontWeight: 'var(--font-weight-semibold)' }}>
            Sign In
          </a>
        </p>
      </Card>
    </div>
  );
};

export default Signup;
