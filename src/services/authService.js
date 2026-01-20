/**
 * Authentication Service - Handles user login/signup and session management
 * Uses localStorage for MVP (no real backend)
 */

import { saveUserProfile, getUserProfile } from './storageService';

/**
 * Validate email format
 */
const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

/**
 * Validate password strength
 */
const isValidPassword = (password) => {
  return password.length >= 6;
};

/**
 * Sign up new user
 * @param {Object} credentials - { email, password, name }
 * @returns {Object} { success: boolean, error: string | null, user: Object }
 */
export const signup = (credentials) => {
  const { email, password, name } = credentials;

  // Validation
  if (!email || !password || !name) {
    return { success: false, error: 'All fields are required' };
  }

  if (!isValidEmail(email)) {
    return { success: false, error: 'Invalid email format' };
  }

  if (!isValidPassword(password)) {
    return { success: false, error: 'Password must be at least 6 characters' };
  }

  // Check if user already exists (in real app, would check backend)
  const existingUser = getUserProfile();
  if (existingUser && existingUser.email === email) {
    return { success: false, error: 'Email already registered' };
  }

  // Create new user
  const newUser = {
    id: Date.now().toString(),
    email,
    name,
    createdAt: new Date().toISOString(),
    storageQuota: 10 * 1024 * 1024 * 1024, // 10 GB quota
    isVerified: true // MVP: auto-verified
  };

  // Save user (in real app, would hash password and store on backend)
  try {
    saveUserProfile(newUser);
    return { success: true, user: newUser };
  } catch (error) {
    return { success: false, error: 'Failed to create account' };
  }
};

/**
 * Login user
 * @param {Object} credentials - { email, password }
 * @returns {Object} { success: boolean, error: string | null, user: Object }
 */
export const login = (credentials) => {
  const { email, password } = credentials;

  // Validation
  if (!email || !password) {
    return { success: false, error: 'Email and password are required' };
  }

  // Retrieve stored user (MVP simulation)
  const storedUser = getUserProfile();

  if (!storedUser) {
    return { success: false, error: 'User not found. Please sign up first.' };
  }

  // Check credentials (MVP: simple comparison, no hashing)
  if (storedUser.email !== email) {
    return { success: false, error: 'Invalid email or password' };
  }

  // Password stored as plain text in MVP (NEVER do this in production!)
  // In real app: use bcrypt or similar for password hashing
  const userPasswordKey = `password_${storedUser.id}`;
  const storedPassword = localStorage.getItem(userPasswordKey);

  if (storedPassword !== password) {
    return { success: false, error: 'Invalid email or password' };
  }

  return { success: true, user: storedUser };
};

/**
 * Save password temporarily (MVP only - DO NOT use in production)
 * In production, use proper password hashing (bcrypt, argon2, etc.)
 */
export const savePasswordTemporarily = (userId, password) => {
  localStorage.setItem(`password_${userId}`, password);
};

/**
 * Check if user is authenticated
 */
export const isAuthenticated = () => {
  const user = getUserProfile();
  return !!user;
};

/**
 * Get current authenticated user
 */
export const getCurrentUser = () => {
  return getUserProfile();
};

/**
 * Logout user
 */
export const logout = () => {
  try {
    const user = getUserProfile();
    if (user) {
      localStorage.removeItem(`password_${user.id}`);
    }
    localStorage.removeItem('secureshare_user');
    return true;
  } catch (error) {
    console.error('Logout error:', error);
    return false;
  }
};

export default {
  signup,
  login,
  isAuthenticated,
  getCurrentUser,
  logout,
  savePasswordTemporarily
};
