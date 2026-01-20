# SecureShare Frontend - React MVP

A modern, decentralized AI-based file sharing platform built with React and Vite.

## 🚀 Quick Start

### Prerequisites
- Node.js 16+
- npm or yarn

### Installation

```bash
cd secureshare
npm install
npm run dev
```

The app will open at `http://localhost:3000`

## 📁 Project Structure

```
secureshare/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── Navbar.jsx
│   │   ├── Button.jsx
│   │   ├── Input.jsx
│   │   ├── Card.jsx
│   │   ├── Alert.jsx
│   │   ├── FileCard.jsx
│   │   └── Footer.jsx
│   ├── pages/               # Page components (routing)
│   │   ├── Landing.jsx
│   │   ├── Login.jsx
│   │   ├── Signup.jsx
│   │   ├── Dashboard.jsx
│   │   ├── FileUpload.jsx
│   │   └── MyFiles.jsx
│   ├── services/            # Business logic & data management
│   │   ├── authService.js   # Authentication & session management
│   │   ├── fileService.js   # File validation & AI labels
│   │   └── storageService.js # localStorage management
│   ├── utils/               # Helper functions
│   │   └── helpers.js
│   ├── styles/              # CSS files
│   │   ├── globals.css      # Global styles & design system
│   │   └── components.css   # Component-specific styles
│   ├── App.jsx              # Main app component & routing
│   └── main.jsx             # React entry point
├── public/                  # Static assets
├── index.html               # HTML template
├── package.json             # Dependencies
├── vite.config.js           # Vite configuration
└── README.md
```

## 🎯 Features

### ✅ Implemented
- **Landing Page** - Hero section with features and CTAs
- **Authentication** - Sign up & login with validation (MVP)
- **Dashboard** - User profile, storage stats, and quick actions
- **File Upload** - Drag-and-drop, MIME type validation, duplicate prevention
- **AI Labels** - Mock AI categorization of uploaded files
- **My Files** - View, filter, sort, and delete uploaded files
- **File Sharing** - Generate and copy IPFS-style content-addressed hashes
- **Responsive Design** - Mobile-first, works on all devices
- **Modern UI** - FAANG-style design with Flexbox/Grid layouts
- **localStorage Integration** - Secure client-side file metadata storage
- **Accessibility** - Semantic HTML, ARIA labels, keyboard navigation

### 🔐 Security & Privacy
- Client-side file handling (files never leave your device)
- localStorage for MVP (no backend exposure)
- Mock IPFS hashes for content-addressed storage
- Duplicate file detection within 1 minute window
- Simulated end-to-end encryption concepts

## 🤖 AI Label Generation

Files are automatically labeled using rule-based AI simulation:
- **Image** → "Photo", "Graphic", "Visual Content"
- **Document** → "Text Document", "Report", "Written Content"
- **Spreadsheet** → "Data Table", "Financial Report", "Analytics"
- **Archive** → "Compressed Files", "Backup Bundle"
- **Video** → "Video Media", "Recording"
- **Audio** → "Audio Recording", "Music"

Special patterns detected:
- `report` → 📊 Financial Report
- `presentation` → 🎯 Presentation
- `contract` → 📋 Contract/Agreement
- `invoice` → 💰 Invoice
- `resume/cv` → 👔 Resume/CV
- `backup` → 💾 Backup Data
- `screenshot` → 📸 Screenshot

## 📦 File Handling

### MIME Type Validation
Supported file types:
- **Images**: JPEG, PNG, GIF
- **Documents**: PDF, TXT, DOC, DOCX
- **Spreadsheets**: XLS, XLSX
- **Archives**: ZIP
- **Media**: MP4, MP3

Max file size: **100 MB**

### Content-Addressed Storage (IPFS Simulation)
Each file is stored with a mock IPFS hash:
```
Qm + 44 random characters
Example: QmX1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s
```

In production, this would integrate with actual IPFS for truly decentralized storage.

## 🔑 Demo Account (Testing)

For quick testing without creating an account:
- **Email**: demo@test.com
- **Password**: demo123

To create an account:
1. Click "Sign Up" on the landing page
2. Enter your details (email, password, name)
3. You'll be redirected to the dashboard

## 🎨 Design System

### Colors
- **Primary**: #6366f1 (Indigo)
- **Success**: #10b981 (Green)
- **Danger**: #ef4444 (Red)
- **Warning**: #f59e0b (Amber)

### Spacing
- 4px (xs) → 64px (3xl)

### Typography
- System font stack
- Responsive font sizes
- Semantic HTML structure

## 📱 Responsive Breakpoints
- Mobile: < 768px (single column)
- Tablet: 768px - 1024px (2 columns)
- Desktop: > 1024px (3-4 columns)

## 🔗 API Simulation

All "API calls" are simulated using localStorage:
- No backend required
- No authentication server
- All data stored locally in browser
- Perfect for MVP/hackathon testing

## 🚀 Build & Deploy

### Development
```bash
npm run dev
```

### Production Build
```bash
npm run build
```

### Preview Build
```bash
npm run preview
```

### Deploy to Vercel
```bash
npm install -g vercel
vercel
```

## 📝 TODO / Future Enhancements

- [ ] Real IPFS integration for decentralized storage
- [ ] Actual AI model for file labeling
- [ ] End-to-end encryption (WebCrypto API)
- [ ] File sharing with permission management
- [ ] Real authentication with JWT
- [ ] Backend API integration
- [ ] File versioning & history
- [ ] Collaborative features
- [ ] Dark mode toggle
- [ ] Multi-language support
- [ ] Search functionality
- [ ] File preview (PDF, images, etc.)
- [ ] Bandwidth monitoring
- [ ] Activity logs

## 🛠️ Tech Stack

- **Frontend**: React 18
- **Build Tool**: Vite
- **Routing**: React Router v6
- **Styling**: CSS3 (Grid, Flexbox, CSS Variables)
- **State Management**: React Hooks (useState, useEffect)
- **Storage**: Browser localStorage (MVP)
- **Deployment**: Vercel/Netlify ready

## 📚 Code Comments

All components and services include detailed comments explaining:
- Purpose of each component
- How state management works
- Validation logic
- Storage operations
- IPFS simulation concepts

## 🤝 Contributing

This is a hackathon MVP. For production use:
1. Add real authentication
2. Integrate backend API
3. Implement proper encryption
4. Add comprehensive error handling
5. Implement rate limiting
6. Add security headers
7. Audit dependencies

## 📄 License

MIT - Feel free to use for hackathons, learning, or personal projects.

## 💬 Support

For questions or issues:
1. Check the code comments
2. Review the service implementations
3. Test with the demo account
4. Inspect browser localStorage in DevTools

---

Built with ❤️ for the SecureShare hackathon MVP
