/**
 * Storage Service - Manages all localStorage operations for files and user data
 * Simulates backend file metadata storage with mock content-addressed storage (IPFS-style)
 */

const STORAGE_KEYS = {
  USER: 'secureshare_user',
  FILES: 'secureshare_files',
  SESSION: 'secureshare_session'
};

/**
 * Mock hash generator - simulates IPFS content-addressed storage
 * In production, this would be replaced with actual IPFS hash generation
 */
const generateMockHash = (file) => {
  const timestamp = Date.now();
  const random = Math.random().toString(36).substring(2, 8);
  return `Qm${random}${timestamp}`.substring(0, 46); // IPFS hash format: Qm + 44 chars
};

/**
 * Retrieve all stored files from localStorage
 */
export const getFiles = () => {
  try {
    const files = localStorage.getItem(STORAGE_KEYS.FILES);
    return files ? JSON.parse(files) : [];
  } catch (error) {
    console.error('Error retrieving files:', error);
    return [];
  }
};

/**
 * Add a new file to storage
 * @param {Object} fileMetadata - File metadata object { name, size, type, aiLabel }
 * @returns {Object} The stored file object with generated hash
 */
export const addFile = (fileMetadata) => {
  try {
    const files = getFiles();
    const newFile = {
      id: Date.now(),
      hash: generateMockHash(fileMetadata), // Content-addressed storage ID
      name: fileMetadata.name,
      size: fileMetadata.size,
      type: fileMetadata.type,
      aiLabel: fileMetadata.aiLabel,
      uploadedAt: new Date().toISOString(),
      isPrivate: true
    };

    // Prevent duplicate file uploads (same name + size + type within 1 minute)
    const isDuplicate = files.some(
      (f) =>
        f.name === newFile.name &&
        f.size === newFile.size &&
        f.type === newFile.type &&
        new Date(f.uploadedAt).getTime() > Date.now() - 60000 // Within last 1 minute
    );

    if (isDuplicate) {
      throw new Error('Duplicate file upload detected. Please wait before uploading the same file again.');
    }

    files.push(newFile);
    localStorage.setItem(STORAGE_KEYS.FILES, JSON.stringify(files));
    return newFile;
  } catch (error) {
    console.error('Error adding file:', error);
    throw error;
  }
};

/**
 * Delete a file from storage
 */
export const deleteFile = (fileId) => {
  try {
    const files = getFiles();
    const updatedFiles = files.filter((f) => f.id !== fileId);
    localStorage.setItem(STORAGE_KEYS.FILES, JSON.stringify(updatedFiles));
    return true;
  } catch (error) {
    console.error('Error deleting file:', error);
    throw error;
  }
};

/**
 * Get user profile from localStorage
 */
export const getUserProfile = () => {
  try {
    const user = localStorage.getItem(STORAGE_KEYS.USER);
    return user ? JSON.parse(user) : null;
  } catch (error) {
    console.error('Error retrieving user profile:', error);
    return null;
  }
};

/**
 * Save user profile to localStorage
 */
export const saveUserProfile = (userProfile) => {
  try {
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(userProfile));
    return true;
  } catch (error) {
    console.error('Error saving user profile:', error);
    throw error;
  }
};

/**
 * Calculate total storage used by user (in bytes)
 */
export const getTotalStorageUsed = () => {
  const files = getFiles();
  return files.reduce((total, file) => total + file.size, 0);
};

/**
 * Format storage size for display (bytes to MB/GB)
 */
export const formatStorageSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
};

/**
 * Clear all user data (logout)
 */
export const clearAllData = () => {
  try {
    localStorage.removeItem(STORAGE_KEYS.USER);
    localStorage.removeItem(STORAGE_KEYS.FILES);
    localStorage.removeItem(STORAGE_KEYS.SESSION);
    return true;
  } catch (error) {
    console.error('Error clearing data:', error);
    throw error;
  }
};

export default {
  getFiles,
  addFile,
  deleteFile,
  getUserProfile,
  saveUserProfile,
  getTotalStorageUsed,
  formatStorageSize,
  clearAllData
};
