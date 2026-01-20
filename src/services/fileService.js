/**
 * File Service - Handles file validation, metadata extraction, and AI label generation
 */

// Allowed MIME types for upload
const ALLOWED_MIME_TYPES = {
  'image/jpeg': { ext: 'jpg', category: 'Image' },
  'image/png': { ext: 'png', category: 'Image' },
  'image/gif': { ext: 'gif', category: 'Image' },
  'application/pdf': { ext: 'pdf', category: 'Document' },
  'text/plain': { ext: 'txt', category: 'Document' },
  'application/msword': { ext: 'doc', category: 'Document' },
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document': { ext: 'docx', category: 'Document' },
  'application/vnd.ms-excel': { ext: 'xls', category: 'Spreadsheet' },
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': { ext: 'xlsx', category: 'Spreadsheet' },
  'application/zip': { ext: 'zip', category: 'Archive' },
  'video/mp4': { ext: 'mp4', category: 'Video' },
  'audio/mpeg': { ext: 'mp3', category: 'Audio' }
};

// Maximum file size: 100 MB
const MAX_FILE_SIZE = 100 * 1024 * 1024;

/**
 * Validate file type using MIME type
 * @param {File} file - The file object
 * @returns {Object} { valid: boolean, error: string | null }
 */
export const validateFileType = (file) => {
  if (!file) {
    return { valid: false, error: 'No file provided' };
  }

  const mimeType = file.type;
  const isValidType = mimeType in ALLOWED_MIME_TYPES || mimeType === '';

  if (!isValidType) {
    return {
      valid: false,
      error: `File type '${mimeType}' is not allowed. Allowed types: images, PDFs, documents, spreadsheets, archives, and videos.`
    };
  }

  return { valid: true };
};

/**
 * Validate file size
 * @param {File} file - The file object
 * @returns {Object} { valid: boolean, error: string | null }
 */
export const validateFileSize = (file) => {
  if (file.size > MAX_FILE_SIZE) {
    return {
      valid: false,
      error: `File size (${(file.size / 1024 / 1024).toFixed(2)} MB) exceeds maximum allowed size (100 MB)`
    };
  }

  return { valid: true };
};

/**
 * Validate file (comprehensive check)
 * @param {File} file - The file object
 * @returns {Object} { valid: boolean, error: string | null }
 */
export const validateFile = (file) => {
  const typeValidation = validateFileType(file);
  if (!typeValidation.valid) return typeValidation;

  const sizeValidation = validateFileSize(file);
  if (!sizeValidation.valid) return sizeValidation;

  return { valid: true };
};

/**
 * Extract file metadata
 * @param {File} file - The file object
 * @returns {Object} Metadata object { name, size, type, category }
 */
export const extractFileMetadata = (file) => {
  return {
    name: file.name,
    size: file.size,
    type: file.type,
    category: ALLOWED_MIME_TYPES[file.type]?.category || 'Unknown',
    extension: file.name.split('.').pop().toUpperCase()
  };
};

/**
 * Mock AI label generator - Simulates privacy-safe AI categorization
 * In production, this would call an actual AI API (OpenAI, etc.)
 * @param {File} file - The file object
 * @returns {string} AI-generated label
 */
export const generateAILabel = (file) => {
  const metadata = extractFileMetadata(file);
  const category = metadata.category;
  const fileName = file.name.toLowerCase();

  // Rule-based label generation (simulates AI output)
  const labelMap = {
    'Image': ['Photo', 'Graphic', 'Visual Content'],
    'Document': ['Text Document', 'Report', 'Written Content'],
    'Spreadsheet': ['Data Table', 'Financial Report', 'Analytics'],
    'Archive': ['Compressed Files', 'Backup Bundle'],
    'Video': ['Video Media', 'Recording'],
    'Audio': ['Audio Recording', 'Music']
  };

  const categoryLabels = labelMap[category] || ['File'];
  const randomLabel = categoryLabels[Math.floor(Math.random() * categoryLabels.length)];

  // Add specific label based on filename keywords
  if (fileName.includes('report')) return '📊 Financial Report';
  if (fileName.includes('presentation')) return '🎯 Presentation';
  if (fileName.includes('contract')) return '📋 Contract/Agreement';
  if (fileName.includes('invoice')) return '💰 Invoice';
  if (fileName.includes('resume') || fileName.includes('cv')) return '👔 Resume/CV';
  if (fileName.includes('backup')) return '💾 Backup Data';
  if (fileName.includes('screenshot')) return '📸 Screenshot';

  return `${randomLabel} (${metadata.extension})`;
};

/**
 * Format file size for display
 * @param {number} bytes - File size in bytes
 * @returns {string} Formatted file size
 */
export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
};

export default {
  validateFile,
  validateFileType,
  validateFileSize,
  extractFileMetadata,
  generateAILabel,
  formatFileSize,
  ALLOWED_MIME_TYPES,
  MAX_FILE_SIZE
};
