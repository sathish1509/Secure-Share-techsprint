/**
 * Utility functions for routing and common helpers
 */

/**
 * Client-side routing helper (simple route resolution)
 * In production, this would be handled by React Router
 */
export const routes = {
  HOME: '/',
  LOGIN: '/login',
  SIGNUP: '/signup',
  DASHBOARD: '/dashboard',
  UPLOAD: '/upload',
  MY_FILES: '/my-files'
};

/**
 * Navigate to a route (handled by React Router in actual app)
 */
export const navigate = (path, navigate) => {
  navigate(path);
};

/**
 * Format date for display
 */
export const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

/**
 * Truncate long strings with ellipsis
 */
export const truncateString = (str, length = 50) => {
  return str.length > length ? str.substring(0, length) + '...' : str;
};

/**
 * Generate random color for avatars
 */
export const getRandomColor = (seed) => {
  const colors = [
    '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
    '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B739', '#52C0A1'
  ];
  const index = (seed ? seed.charCodeAt(0) : 0) % colors.length;
  return colors[index];
};

export default {
  routes,
  navigate,
  formatDate,
  truncateString,
  getRandomColor
};
