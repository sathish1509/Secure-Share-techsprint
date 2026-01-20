# 🏗️ SecureShare Frontend - Architecture Overview

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        BROWSER (Client-Side)                 │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              React Application (React 18)             │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │                                                        │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │          React Router (Page Routing)           │  │   │
│  │  │                                                 │  │   │
│  │  │  Landing → /      (Public)                     │  │   │
│  │  │  Signup  → /signup (Public)                    │  │   │
│  │  │  Login   → /login  (Public)                    │  │   │
│  │  │  Dashboard → /dashboard (Protected)            │  │   │
│  │  │  Upload → /upload (Protected)                  │  │   │
│  │  │  MyFiles → /my-files (Protected)               │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  │                        ↓                              │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │         Layout Components (Navbar, Footer)      │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  │                        ↓                              │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │       Page Components (Landing, Login, etc.)    │  │   │
│  │  │                                                 │  │   │
│  │  │  Uses:                                         │  │   │
│  │  │  ├─ Reusable UI Components (Button, Input, etc)│  │   │
│  │  │  ├─ Service Functions (auth, file, storage)    │  │   │
│  │  │  └─ React Hooks (useState, useEffect)         │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  │                        ↓                              │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │       Service Layer (Business Logic)            │  │   │
│  │  │                                                 │  │   │
│  │  │  authService.js                                │  │   │
│  │  │  ├─ signup()                                   │  │   │
│  │  │  ├─ login()                                    │  │   │
│  │  │  └─ logout()                                   │  │   │
│  │  │                                                 │  │   │
│  │  │  fileService.js                                │  │   │
│  │  │  ├─ validateFile()                             │  │   │
│  │  │  ├─ generateAILabel()                          │  │   │
│  │  │  └─ formatFileSize()                           │  │   │
│  │  │                                                 │  │   │
│  │  │  storageService.js                             │  │   │
│  │  │  ├─ getFiles()                                 │  │   │
│  │  │  ├─ addFile()                                  │  │   │
│  │  │  └─ deleteFile()                               │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  │                        ↓                              │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │     localStorage (Client-Side Persistence)      │  │   │
│  │  │                                                 │  │   │
│  │  │  secureshare_user  → User profile             │  │   │
│  │  │  secureshare_files → File metadata array      │  │   │
│  │  │  password_*        → Stored passwords (MVP)    │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  │                                                        │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │            CSS & Design System                       │   │
│  │  ├─ CSS Variables (colors, spacing, typography)     │   │
│  │  ├─ Utility Classes (flexbox, grid, spacing)        │   │
│  │  ├─ Responsive Design (mobile-first)               │   │
│  │  └─ Component Styles (buttons, forms, etc.)        │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ (No Real Backend - MVP Only)
                              │
        ┌─────────────────────────────────────────┐
        │   Production Mode (Optional Backend)    │
        ├─────────────────────────────────────────┤
        │  API Server (Node.js / Python / etc.)   │
        │  Database (PostgreSQL / MongoDB)        │
        │  File Storage (S3 / IPFS)               │
        └─────────────────────────────────────────┘
```

---

## Data Flow Architecture

### **1. Authentication Flow**

```
User clicks "Sign Up"
    ↓
Signup page renders form
    ↓
User enters: name, email, password
    ↓
Form validation (frontend)
    ↓
User clicks "Sign Up" button
    ↓
handleSubmit() → authService.signup()
    ↓
signup() validates input
    ├─ Email format ✓
    ├─ Password length ✓
    └─ Check if user exists (localStorage)
    ↓
If valid:
    ├─ Create user object with ID
    ├─ Save to localStorage: secureshare_user
    ├─ Save password: password_[userId]
    ├─ Return success
    ↓
Component receives success
    ├─ Set alert (success message)
    ├─ Update parent state (setUser)
    ├─ Wait 2 seconds
    ├─ Redirect to /dashboard
    ↓
Dashboard loads with user data
    ├─ Calls getUserProfile() from localStorage
    ├─ Displays user profile
    ├─ Shows storage stats
```

### **2. File Upload Flow**

```
User selects/drags file to upload area
    ↓
handleDrop() or handleFileSelect() triggered
    ↓
processFile(file) → fileService.validateFile()
    ├─ Check MIME type (allowed?)
    ├─ Check file size (< 100 MB?)
    └─ Return { valid: bool, error: string }
    ↓
If validation fails:
    ├─ Show error alert
    ├─ Stop processing
    ↓
If valid:
    ├─ Set selectedFile state
    ├─ If image: generate preview with FileReader
    ├─ Show file preview & metadata
    ├─ Generate AI label with generateAILabel()
    ↓
User clicks "Upload File" button
    ↓
handleUpload() triggered
    ├─ generateAILabel(file) → mock AI categorization
    ├─ Create metadata object:
    │  {
    │    name: "document.pdf",
    │    size: 2048576,
    │    type: "application/pdf",
    │    aiLabel: "📊 Financial Report"
    │  }
    ├─ Call storageService.addFile(metadata)
    ├─ addFile() generates mock IPFS hash
    ├─ Stores file metadata in localStorage
    └─ Returns uploaded file object
    ↓
Upload completes
    ├─ Show success alert
    ├─ Clear form state
    ├─ Wait 2 seconds
    ├─ Redirect to /my-files
    ↓
MyFiles page loads
    ├─ Calls getFiles() from localStorage
    ├─ Renders FileCard components
    ├─ Displays file metadata with AI label
```

### **3. File Listing & Management Flow**

```
User navigates to /my-files
    ↓
MyFiles component mounts
    ├─ useEffect hook runs
    ├─ Calls getFiles() from localStorage
    ├─ Sets files state
    ↓
Files display with filters & sort
    ├─ User selects filter (e.g., "Images")
    ├─ User selects sort (e.g., "Largest First")
    ├─ applyFiltersAndSort() function:
    │  ├─ Filter files by type
    │  ├─ Sort by selected option
    │  └─ Update filteredFiles state
    ├─ Component re-renders with filtered/sorted data
    ↓
User sees FileCard components for each file
    ├─ File icon
    ├─ Name, size, date
    ├─ AI label
    ├─ Content hash preview
    ├─ Action buttons
    ↓
User clicks "Delete" button
    ├─ Show confirmation dialog
    ├─ If confirmed:
    │  ├─ Call deleteFile(fileId)
    │  ├─ Filter from localStorage
    │  ├─ Reload files
    │  ├─ Re-render component
    │  └─ Show success alert
    ↓
User clicks "Share" button
    ├─ Open share modal
    ├─ Display content-addressed hash
    ├─ Show share link (secureshare://share/hash)
    ├─ User clicks "Copy" button
    ├─ Copy to clipboard with navigator.clipboard.writeText()
    ├─ Show "Copied" confirmation
```

---

## Component Hierarchy

```
App.jsx (Root)
├─ Navbar
│  ├─ Logo & Brand
│  ├─ Navigation Links (conditional by auth)
│  └─ User Menu (conditional)
│
├─ Main Routes (React Router)
│  │
│  ├─ Landing (/)
│  │  ├─ Hero Section
│  │  ├─ Features Grid (3 Cards)
│  │  │  └─ Card components (x3)
│  │  ├─ How It Works (3 steps)
│  │  └─ CTA Section
│  │
│  ├─ Signup (/signup) [Protected: redirect if logged in]
│  │  └─ Card
│  │     ├─ Form
│  │     │  ├─ Input (name)
│  │     │  ├─ Input (email)
│  │     │  ├─ Input (password)
│  │     │  ├─ Input (confirm password)
│  │     │  └─ Button (submit)
│  │     ├─ Alert (error/success)
│  │     └─ Link to Login
│  │
│  ├─ Login (/login) [Protected: redirect if logged in]
│  │  └─ Card
│  │     ├─ Form
│  │     │  ├─ Input (email)
│  │     │  ├─ Input (password)
│  │     │  └─ Button (submit)
│  │     ├─ Alert (error/success)
│  │     ├─ Link to Signup
│  │     └─ Demo Account Info
│  │
│  ├─ Dashboard (/dashboard) [Protected]
│  │  ├─ Profile Card
│  │  │  ├─ Avatar (getRandomColor)
│  │  │  ├─ Name
│  │  │  └─ Email
│  │  │
│  │  ├─ Quick Actions (2 Cards)
│  │  │  ├─ Upload Button
│  │  │  └─ View Files Button
│  │  │
│  │  ├─ Statistics Grid (3 Cards)
│  │  │  ├─ Card (total files)
│  │  │  ├─ Card (storage used)
│  │  │  └─ Card (quota)
│  │  │
│  │  ├─ Storage Bar (Card)
│  │  │  └─ Progress bar
│  │  │
│  │  └─ Features Grid (4 Cards)
│  │     └─ Card components (x4)
│  │
│  ├─ Upload (/upload) [Protected]
│  │  ├─ Alert (multiple)
│  │  ├─ Drag-drop zone
│  │  ├─ File input (hidden)
│  │  ├─ File Preview (conditional)
│  │  │  ├─ Image preview (if image)
│  │  │  ├─ Metadata grid
│  │  │  ├─ Button (upload)
│  │  │  └─ Button (clear)
│  │  └─ How It Works Card
│  │
│  └─ MyFiles (/my-files) [Protected]
│     ├─ File counter & storage info
│     ├─ Upload button
│     ├─ Filters & Sort
│     │  ├─ Filter dropdown
│     │  └─ Sort dropdown
│     ├─ File Cards Grid (2 columns)
│     │  └─ FileCard (x N)
│     │     ├─ File icon
│     │     ├─ Metadata display
│     │     └─ Action buttons
│     ├─ Empty State (conditional)
│     └─ Share Modal (conditional)
│        ├─ Hash display
│        ├─ Copy button
│        ├─ Share link display
│        └─ Close button
│
└─ Footer
   ├─ Info section
   ├─ Quick links
   ├─ Contact info
   └─ Copyright
```

---

## State Management Strategy

### **Global State** (App.jsx)
```javascript
const [user, setUser] = useState(null);
const [loading, setLoading] = useState(true);

// Initialized from localStorage on mount:
useEffect(() => {
  const currentUser = getUserProfile();
  if (currentUser) setUser(currentUser);
  setLoading(false);
}, []);
```

### **Component Local State** (Examples)

**FileUpload.jsx**:
```javascript
const [dragActive, setDragActive] = useState(false);
const [selectedFile, setSelectedFile] = useState(null);
const [preview, setPreview] = useState(null);
const [uploading, setUploading] = useState(false);
const [alerts, setAlerts] = useState([]);
```

**MyFiles.jsx**:
```javascript
const [files, setFiles] = useState([]);
const [filteredFiles, setFilteredFiles] = useState([]);
const [filter, setFilter] = useState('all');
const [sortBy, setSortBy] = useState('recent');
const [alerts, setAlerts] = useState([]);
const [shareModal, setShareModal] = useState(null);
```

**Pattern**: No Redux/Zustand needed for MVP - useState sufficient.

---

## Service Layer Pattern

### **Dependency Inversion**
```
Components → Services → localStorage
```

### **Services are Pure Functions**
```javascript
// No side effects, no state
// Same input → Same output (testable)

export const validateFile = (file) => {
  // Pure function
  return { valid: bool, error: string };
};

export const addFile = (metadata) => {
  // Side effect: localStorage write
  // But all logic is here, not scattered
  const files = getFiles();
  files.push(newFile);
  localStorage.setItem(STORAGE_KEYS.FILES, JSON.stringify(files));
  return newFile;
};
```

### **Easy to Mock for Testing**
```javascript
// In tests, can replace services with mocks
const mockStorage = {
  getFiles: () => [{ name: 'test.pdf' }],
  addFile: (f) => ({ id: 1, ...f })
};
```

---

## Protected Routes Pattern

```javascript
// App.jsx
const ProtectedRoute = ({ children }) => {
  if (loading) return <LoadingSpinner />;
  if (!user) return <Navigate to="/login" replace />;
  return children;
};

// Usage
<Route
  path="/dashboard"
  element={
    <ProtectedRoute>
      <Dashboard user={user} />
    </ProtectedRoute>
  }
/>
```

**Flow**:
1. User not logged in → Redirect to /login
2. User logged in → Show dashboard
3. Loading → Show spinner

---

## Styling Architecture

### **Cascade**
```
globals.css (Base styles, variables, reset)
    ↓
components.css (Layouts, utilities, components)
    ↓
Component JSX (Inline styles if needed, className application)
```

### **CSS Variables Flow**
```
:root { --color-primary: #6366f1; }
    ↓
.btn-primary { background: var(--color-primary); }
    ↓
<Button variant="primary"> → class="btn-primary"
    ↓
Gets var(--color-primary) #6366f1
```

### **Responsive Approach**
```
Mobile-first:
1. Single column by default
2. @media (min-width: 768px) → 2 columns
3. @media (min-width: 1024px) → 3-4 columns
```

---

## Storage Layer Architecture

### **localStorage Structure**
```javascript
{
  secureshare_user: {
    id: "timestamp",
    email: "user@example.com",
    name: "John Doe",
    createdAt: "2024-01-20T...",
    storageQuota: 10737418240  // 10GB
  },

  secureshare_files: [
    {
      id: 1705779234567,
      hash: "QmX1a2b3c4d5e6f...", // IPFS-style
      name: "document.pdf",
      size: 2048576,
      type: "application/pdf",
      aiLabel: "📊 Financial Report",
      uploadedAt: "2024-01-20T10:30:45.123Z",
      isPrivate: true
    },
    // ... more files
  ],

  password_[userId]: "password123"  // MVP only
}
```

### **CRUD Operations**
```
Create: addFile(metadata) → generates hash → saves to localStorage
Read:   getFiles() → parse localStorage → return array
Update: (Not implemented in MVP - could be added)
Delete: deleteFile(id) → filter array → save updated
```

---

## Error Handling Strategy

### **Validation Errors**
```javascript
const validateForm = () => {
  const errors = {};
  if (!email) errors.email = 'Email required';
  if (!isValidEmail(email)) errors.email = 'Invalid format';
  return errors;
};

// Display in component
{error && <span className="form-error">{error}</span>}
```

### **Try-Catch Pattern**
```javascript
try {
  const result = addFile(metadata);
  addAlert('success', 'Upload Complete', 'File uploaded!');
} catch (error) {
  addAlert('danger', 'Upload Failed', error.message);
}
```

### **User Feedback**
```javascript
// Alerts auto-dismiss after 4-5 seconds
const addAlert = (type, title, message) => {
  const id = Date.now();
  setAlerts(prev => [...prev, { id, type, title, message }]);
  setTimeout(() => {
    setAlerts(prev => prev.filter(a => a.id !== id));
  }, 4000);
};
```

---

## Security Considerations

### **Client-Side Only (MVP)**
- ✅ localStorage for MVP (not production)
- ✅ Validation on submit
- ✅ No sensitive data in localStorage (tokens, etc.)
- ⚠️ Password stored plain text (MVP only!)

### **Future (Production)**
- 🔒 HTTPS only
- 🔒 JWT tokens
- 🔒 Password hashing (bcrypt)
- 🔒 Server-side validation
- 🔒 Rate limiting
- 🔒 CORS headers

---

## Performance Optimizations

### **Implemented**
- ✅ React 18 (fast re-renders)
- ✅ Functional components (efficient)
- ✅ Memoization where needed
- ✅ Event delegation (parent clicks)
- ✅ CSS variables (no recalculation)
- ✅ Lazy loading possible (not implemented)

### **Could Add**
- Code splitting per page
- Lazy component loading
- Image optimization
- localStorage size limits
- Service worker caching

---

## Testing Architecture

### **How to Test Each Layer**

**Components**:
```javascript
// Mock services
const mockAuthService = {
  login: jest.fn(() => Promise.resolve({ id: 1 }))
};

// Render component with mock
render(<Login onLogin={mockFn} />);
```

**Services**:
```javascript
// Pure functions - easy to test
const result = validateFile(largeFile);
expect(result.valid).toBe(false);
expect(result.error).toContain('size');
```

**Integration**:
```javascript
// Test full flow
1. Sign up
2. Verify stored in localStorage
3. Login
4. Upload file
5. Verify in MyFiles
6. Delete
7. Verify removed
```

---

## Conclusion

**Architecture Strengths**:
✅ Clear separation of concerns  
✅ Scalable component structure  
✅ Easy to test (services)  
✅ Simple state management  
✅ Responsive design system  
✅ Well-documented code  

**MVP to Production Path**:
1. Keep component structure
2. Replace localStorage with API calls
3. Add backend services
4. Implement real authentication
5. Add encryption layer
6. Deploy to production

Built for clarity, learning, and easy extension.
