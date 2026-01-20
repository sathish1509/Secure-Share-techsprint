/**
 * API_CONCEPTS.js - Backend Integration Guide for SecureShare MVP
 * 
 * This file documents how the MVP simulates API calls using localStorage,
 * and how to integrate with real backends in production.
 */

// ============================================================================
// PART 1: CURRENT MVP ARCHITECTURE (localStorage simulation)
// ============================================================================

/**
 * MVP Pattern: Direct Service Layer → localStorage
 * 
 * Request Flow:
 *   Component → Service Function → JSON.parse/stringify → localStorage
 * 
 * Example: Upload File
 * ─────────────────────────────────────────────────────────────────────────
 */

// Current MVP (storageService.js):
export const addFileMVP = (fileMetadata) => {
  // Simulate file upload by storing metadata locally
  const files = JSON.parse(localStorage.getItem('secureshare_files') || '[]');
  
  const newFile = {
    id: Date.now(),
    hash: generateMockHash(fileMetadata),
    name: fileMetadata.name,
    size: fileMetadata.size,
    type: fileMetadata.type,
    aiLabel: fileMetadata.aiLabel,
    uploadedAt: new Date().toISOString(),
    isPrivate: true
  };
  
  files.push(newFile);
  localStorage.setItem('secureshare_files', JSON.stringify(files));
  
  return newFile;
};

// ============================================================================
// PART 2: PRODUCTION ARCHITECTURE (Backend API)
// ============================================================================

/**
 * Production Pattern: Component → Service → Fetch API → Backend → Database
 * 
 * Request Flow:
 *   UI Action → Service Function → HTTP Request → API Server → DB → Response
 * 
 * Benefits over MVP:
 *   ✅ Scalable (multiple users)
 *   ✅ Secure (hashed passwords, server-side validation)
 *   ✅ Persistent (database)
 *   ✅ Collaborative (share between users)
 *   ✅ Real file storage (S3, IPFS, etc.)
 */

// ─────────────────────────────────────────────────────────────────────────
// Production: Authentication Service
// ─────────────────────────────────────────────────────────────────────────

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://api.secureshare.com';

export const authServiceProduction = {
  /**
   * Sign up new user
   * POST /api/auth/signup
   */
  signup: async (credentials) => {
    const response = await fetch(`${API_BASE_URL}/api/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: credentials.name,
        email: credentials.email,
        password: credentials.password // Should be hashed on frontend
      })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message);
    }

    const { user, token } = await response.json();
    
    // Store JWT token for authenticated requests
    localStorage.setItem('auth_token', token);
    
    return user;
  },

  /**
   * Login user
   * POST /api/auth/login
   */
  login: async (credentials) => {
    const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: credentials.email,
        password: credentials.password
      })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message);
    }

    const { user, token } = await response.json();
    localStorage.setItem('auth_token', token);
    
    return user;
  },

  /**
   * Logout user
   * POST /api/auth/logout
   */
  logout: async () => {
    const token = localStorage.getItem('auth_token');
    
    await fetch(`${API_BASE_URL}/api/auth/logout`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });

    localStorage.removeItem('auth_token');
  }
};

// ─────────────────────────────────────────────────────────────────────────
// Production: File Service
// ─────────────────────────────────────────────────────────────────────────

export const fileServiceProduction = {
  /**
   * Upload file to server
   * POST /api/files/upload
   * 
   * Request:
   *   - file: File object (multipart/form-data)
   *   - name: string
   *   - type: string
   * 
   * Response:
   *   {
   *     id: "file_123abc",
   *     hash: "QmXxxx...",
   *     name: "document.pdf",
   *     size: 2048576,
   *     type: "application/pdf",
   *     aiLabel: "📊 Financial Report",
   *     uploadedAt: "2024-01-20T10:30:45Z",
   *     url: "https://api.secureshare.com/files/file_123abc"
   *   }
   */
  uploadFile: async (file) => {
    const token = localStorage.getItem('auth_token');
    const formData = new FormData();
    formData.append('file', file);
    formData.append('name', file.name);
    formData.append('type', file.type);

    const response = await fetch(`${API_BASE_URL}/api/files/upload`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message);
    }

    return await response.json();
  },

  /**
   * Get all files for user
   * GET /api/files
   */
  getFiles: async () => {
    const token = localStorage.getItem('auth_token');

    const response = await fetch(`${API_BASE_URL}/api/files`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) throw new Error('Failed to fetch files');
    
    return await response.json();
  },

  /**
   * Delete file
   * DELETE /api/files/:fileId
   */
  deleteFile: async (fileId) => {
    const token = localStorage.getItem('auth_token');

    const response = await fetch(`${API_BASE_URL}/api/files/${fileId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) throw new Error('Failed to delete file');
    
    return true;
  }
};

// ============================================================================
// PART 3: MIGRATION STRATEGY (MVP → Production)
// ============================================================================

/**
 * Step-by-step guide to migrate from localStorage to backend:
 * 
 * STEP 1: Create abstraction layer
 * ────────────────────────────────────────────────────────────────────────
 * 
 * Create storageService.js with conditional logic:
 */

const USE_BACKEND = process.env.REACT_APP_USE_BACKEND === 'true';

export const getFilesAbstracted = async () => {
  if (USE_BACKEND) {
    // Call backend API
    return fileServiceProduction.getFiles();
  } else {
    // Use localStorage (MVP)
    return JSON.parse(localStorage.getItem('secureshare_files') || '[]');
  }
};

export const addFileAbstracted = async (fileMetadata) => {
  if (USE_BACKEND) {
    // Create File object and upload
    const file = new File([new Blob()], fileMetadata.name, { type: fileMetadata.type });
    return fileServiceProduction.uploadFile(file);
  } else {
    // Use localStorage (MVP)
    return addFileMVP(fileMetadata);
  }
};

/**
 * STEP 2: Environment configuration
 * ────────────────────────────────────────────────────────────────────────
 * 
 * .env.local (Development - MVP):
 *   REACT_APP_USE_BACKEND=false
 *   REACT_APP_API_URL=http://localhost:5000
 * 
 * .env.production (Production - Backend):
 *   REACT_APP_USE_BACKEND=true
 *   REACT_APP_API_URL=https://api.secureshare.com
 * 
 * Build commands:
 *   npm run dev     # Uses .env.local (MVP mode)
 *   npm run build   # Uses .env.production (Backend mode)
 */

/**
 * STEP 3: Error handling wrapper
 * ────────────────────────────────────────────────────────────────────────
 */

export const withErrorHandling = async (apiCall) => {
  try {
    return await apiCall();
  } catch (error) {
    if (error.message.includes('401')) {
      // Token expired - refresh or redirect to login
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    throw error;
  }
};

// Usage:
export const getFilesSafe = async () => {
  return withErrorHandling(() => getFilesAbstracted());
};

/**
 * STEP 4: Add request/response interceptors
 * ────────────────────────────────────────────────────────────────────────
 */

export const createAPIClient = () => {
  const client = {
    async request(endpoint, options = {}) {
      const token = localStorage.getItem('auth_token');
      const headers = {
        'Content-Type': 'application/json',
        ...options.headers
      };

      if (token && !options.skipAuth) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers
      });

      // Auto-refresh token if expired
      if (response.status === 401) {
        // Attempt token refresh
        const refreshed = await this.refreshToken();
        if (refreshed) {
          // Retry request
          return this.request(endpoint, options);
        }
      }

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message);
      }

      return response.json();
    },

    async refreshToken() {
      try {
        const response = await fetch(`${API_BASE_URL}/api/auth/refresh`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        });
        
        if (response.ok) {
          const { token } = await response.json();
          localStorage.setItem('auth_token', token);
          return true;
        }
      } catch (error) {
        console.error('Token refresh failed:', error);
      }
      return false;
    }
  };

  return client;
};

// ============================================================================
// PART 4: BACKEND REQUIREMENTS (What your server needs to implement)
// ============================================================================

/**
 * API Endpoints Required for Production
 * 
 * Authentication:
 *   POST   /api/auth/signup          - Register new user
 *   POST   /api/auth/login           - Authenticate user
 *   POST   /api/auth/logout          - Invalidate session
 *   POST   /api/auth/refresh         - Refresh JWT token
 *   POST   /api/auth/verify-email    - Verify email address
 * 
 * Files:
 *   POST   /api/files/upload         - Upload new file
 *   GET    /api/files                - List user's files
 *   GET    /api/files/:id            - Get file details
 *   DELETE /api/files/:id            - Delete file
 *   POST   /api/files/:id/share      - Create share link
 *   POST   /api/files/:id/labels     - Generate AI label
 * 
 * User:
 *   GET    /api/user/profile         - Get user profile
 *   PUT    /api/user/profile         - Update profile
 *   GET    /api/user/storage         - Get storage stats
 *   POST   /api/user/password        - Change password
 * 
 * Sharing:
 *   POST   /api/shares               - Create share
 *   GET    /api/shares/:hash         - Access shared file
 *   DELETE /api/shares/:id           - Revoke access
 */

/**
 * Database Schema Example
 * 
 * Users Table:
 *   id: UUID
 *   email: string (unique)
 *   password_hash: string (bcrypt)
 *   name: string
 *   created_at: timestamp
 *   storage_quota: bigint (10GB default)
 *   verified: boolean
 * 
 * Files Table:
 *   id: UUID
 *   user_id: UUID (foreign key)
 *   name: string
 *   type: string (MIME type)
 *   size: bigint
 *   ipfs_hash: string (content address)
 *   ai_label: string
 *   created_at: timestamp
 *   updated_at: timestamp
 *   is_private: boolean
 * 
 * Shares Table:
 *   id: UUID
 *   file_id: UUID (foreign key)
 *   shared_by: UUID (foreign key)
 *   shared_with: string (email)
 *   permission: enum ('view', 'edit', 'comment')
 *   created_at: timestamp
 *   expires_at: timestamp
 */

/**
 * Security Checklist for Backend
 * 
 * ✅ Use HTTPS only (TLS 1.2+)
 * ✅ Hash passwords with bcrypt (at least 10 rounds)
 * ✅ Use JWT tokens with expiration (1 hour)
 * ✅ Implement CORS properly (allow only trusted origins)
 * ✅ Validate all file MIME types server-side
 * ✅ Limit file upload size (100 MB)
 * ✅ Encrypt sensitive data in transit & at rest
 * ✅ Implement rate limiting (prevent brute force)
 * ✅ Use environment variables for secrets
 * ✅ Audit logs for file access
 * ✅ SQL injection prevention (parameterized queries)
 * ✅ XSS prevention (sanitize outputs)
 * ✅ CSRF tokens for state-changing operations
 */

// ============================================================================
// PART 5: TESTING THE MIGRATION
// ============================================================================

/**
 * Integration Test Strategy
 * 
 * Mock Backend (for testing frontend independently):
 * ──────────────────────────────────────────────────
 */

export const mockAPIClient = {
  files: [],
  users: {},

  async request(endpoint, options = {}) {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 500));

    if (endpoint === '/api/files/upload' && options.method === 'POST') {
      const file = {
        id: Math.random().toString(36).substring(7),
        hash: 'QmMockHash...',
        name: 'test.pdf',
        size: 1024,
        aiLabel: '📄 Document'
      };
      this.files.push(file);
      return file;
    }

    if (endpoint === '/api/files' && options.method === 'GET') {
      return this.files;
    }

    throw new Error(`Unknown endpoint: ${endpoint}`);
  }
};

// ============================================================================
// PART 6: MONITORING & ANALYTICS
// ============================================================================

/**
 * Add analytics to track usage:
 * 
 * Events to track:
 *   - User signup
 *   - User login
 *   - File uploaded (+ size, type)
 *   - File deleted
 *   - File shared
 *   - Storage quota reached (80%, 95%)
 *   - Error events (upload failed, etc.)
 */

export const trackEvent = (eventName, data = {}) => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', eventName, data);
  }
  console.log(`📊 Event: ${eventName}`, data);
};

// Usage in components:
/*
const handleFileUpload = async (file) => {
  trackEvent('file_upload_start', { size: file.size });
  try {
    await uploadFile(file);
    trackEvent('file_upload_success', { name: file.name });
  } catch (error) {
    trackEvent('file_upload_error', { error: error.message });
  }
};
*/

// ============================================================================
// SUMMARY
// ============================================================================

/**
 * Current State (MVP):
 * ───────────────────
 * ✅ All data in localStorage
 * ✅ No backend required
 * ✅ Single user/browser
 * ✅ Perfect for hackathon/demo
 * 
 * Next Steps (Production):
 * ────────────────────────
 * 1. Build backend API (Node.js/Python/etc)
 * 2. Set up database (PostgreSQL/MongoDB)
 * 3. Implement authentication (JWT)
 * 4. Set up file storage (S3/IPFS/etc)
 * 5. Add error handling & logging
 * 6. Deploy to production
 * 7. Add monitoring & analytics
 * 8. Scale with CDN & caching
 * 
 * Estimated Backend Build Time: 2-4 weeks
 * Recommended Tech Stack:
 *   - Backend: Node.js + Express (or Python + Flask)
 *   - Database: PostgreSQL
 *   - File Storage: AWS S3 (or IPFS)
 *   - Authentication: JWT + OAuth
 *   - Deployment: Docker + Kubernetes
 */

export default {
  authServiceProduction,
  fileServiceProduction,
  createAPIClient,
  mockAPIClient,
  trackEvent,
  getFilesAbstracted,
  addFileAbstracted
};
