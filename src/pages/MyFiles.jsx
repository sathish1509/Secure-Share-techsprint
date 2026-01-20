import React, { useState, useEffect } from 'react';
import FileCard from '../components/FileCard';
import Card from '../components/Card';
import Button from '../components/Button';
import Alert from '../components/Alert';
import { getFiles, deleteFile, formatStorageSize, getTotalStorageUsed } from '../services/storageService';

/**
 * My Files Page - Display all uploaded files
 */
const MyFiles = () => {
  const [files, setFiles] = useState([]);
  const [filteredFiles, setFilteredFiles] = useState([]);
  const [filter, setFilter] = useState('all');
  const [sortBy, setSortBy] = useState('recent');
  const [alerts, setAlerts] = useState([]);
  const [shareModal, setShareModal] = useState(null);

  useEffect(() => {
    loadFiles();
  }, []);

  useEffect(() => {
    applyFiltersAndSort();
  }, [files, filter, sortBy]);

  const addAlert = (type, title, message) => {
    const id = Date.now();
    setAlerts((prev) => [...prev, { id, type, title, message }]);
    setTimeout(() => {
      setAlerts((prev) => prev.filter((a) => a.id !== id));
    }, 4000);
  };

  const loadFiles = () => {
    const loadedFiles = getFiles();
    setFiles(loadedFiles);
  };

  const applyFiltersAndSort = () => {
    let result = [...files];

    // Apply filter
    if (filter !== 'all') {
      result = result.filter((file) => {
        if (filter === 'image') return file.type.startsWith('image/');
        if (filter === 'document') return file.type.includes('document') || file.type.includes('word') || file.type === 'application/pdf';
        if (filter === 'spreadsheet') return file.type.includes('sheet') || file.type.includes('excel');
        if (filter === 'video') return file.type.startsWith('video/');
        if (filter === 'audio') return file.type.startsWith('audio/');
        return true;
      });
    }

    // Apply sort
    if (sortBy === 'recent') {
      result.sort((a, b) => new Date(b.uploadedAt) - new Date(a.uploadedAt));
    } else if (sortBy === 'name-asc') {
      result.sort((a, b) => a.name.localeCompare(b.name));
    } else if (sortBy === 'name-desc') {
      result.sort((a, b) => b.name.localeCompare(a.name));
    } else if (sortBy === 'size-asc') {
      result.sort((a, b) => a.size - b.size);
    } else if (sortBy === 'size-desc') {
      result.sort((a, b) => b.size - a.size);
    }

    setFilteredFiles(result);
  };

  const handleDelete = (fileId) => {
    if (confirm('Are you sure you want to delete this file? This action cannot be undone.')) {
      try {
        deleteFile(fileId);
        loadFiles();
        addAlert('success', 'File Deleted', 'The file has been removed from your storage.');
      } catch (error) {
        addAlert('danger', 'Delete Failed', error.message);
      }
    }
  };

  const handleShare = (file) => {
    setShareModal(file);
    addAlert('info', 'Share Link Generated', `Copy the link below to share this file with others.`);
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    addAlert('success', 'Copied', 'Share link copied to clipboard!');
  };

  const totalStorage = getTotalStorageUsed();

  return (
    <div className="container">
      <div style={{ marginBottom: 'var(--space-2xl)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 'var(--space-md)' }}>
          <div>
            <h1 style={{ marginBottom: 'var(--space-sm)' }}>My Files</h1>
            <p className="text-small">
              {filteredFiles.length} file{filteredFiles.length !== 1 ? 's' : ''} • {formatStorageSize(totalStorage)} used
            </p>
          </div>
          <a href="/upload" className="btn btn-primary">
            📤 Upload New File
          </a>
        </div>
      </div>

      {/* Alerts */}
      <div style={{ marginBottom: 'var(--space-lg)' }}>
        {alerts.map((alert) => (
          <Alert
            key={alert.id}
            type={alert.type}
            title={alert.title}
            message={alert.message}
            onClose={() => setAlerts((prev) => prev.filter((a) => a.id !== alert.id))}
          />
        ))}
      </div>

      {/* Filters and Sort */}
      <Card style={{ marginBottom: 'var(--space-lg)' }}>
        <div style={{ display: 'flex', gap: 'var(--space-md)', flexWrap: 'wrap', alignItems: 'center' }}>
          <div>
            <label className="form-label" style={{ marginBottom: '0' }}>Filter:</label>
            <select value={filter} onChange={(e) => setFilter(e.target.value)} className="form-select" style={{ width: 'auto' }}>
              <option value="all">All Files</option>
              <option value="image">Images</option>
              <option value="document">Documents</option>
              <option value="spreadsheet">Spreadsheets</option>
              <option value="video">Videos</option>
              <option value="audio">Audio</option>
            </select>
          </div>

          <div>
            <label className="form-label" style={{ marginBottom: '0' }}>Sort by:</label>
            <select value={sortBy} onChange={(e) => setSortBy(e.target.value)} className="form-select" style={{ width: 'auto' }}>
              <option value="recent">Most Recent</option>
              <option value="name-asc">Name (A-Z)</option>
              <option value="name-desc">Name (Z-A)</option>
              <option value="size-asc">Size (Smallest First)</option>
              <option value="size-desc">Size (Largest First)</option>
            </select>
          </div>
        </div>
      </Card>

      {/* Files Grid */}
      {filteredFiles.length === 0 ? (
        <Card style={{ textAlign: 'center', padding: 'var(--space-2xl)' }}>
          <div style={{ fontSize: '48px', marginBottom: 'var(--space-md)' }}>📁</div>
          <h3>No Files Yet</h3>
          <p style={{ marginBottom: 'var(--space-lg)' }}>
            {files.length === 0 ? 'You haven\'t uploaded any files yet.' : 'No files match your filter.'}
          </p>
          <a href="/upload" className="btn btn-primary">
            Upload Your First File
          </a>
        </Card>
      ) : (
        <div className="grid-cols-2">
          {filteredFiles.map((file) => (
            <FileCard
              key={file.id}
              file={file}
              onDelete={handleDelete}
              onShare={handleShare}
            />
          ))}
        </div>
      )}

      {/* Share Modal */}
      {shareModal && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0, 0, 0, 0.5)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000
        }}>
          <Card style={{ maxWidth: '500px', width: '90%' }}>
            <h3 style={{ marginBottom: 'var(--space-lg)' }}>Share File: {shareModal.name}</h3>

            <div style={{ background: 'var(--color-bg-secondary)', padding: 'var(--space-lg)', borderRadius: 'var(--radius-md)', marginBottom: 'var(--space-lg)' }}>
              <p className="text-small" style={{ color: 'var(--color-text-secondary)', marginBottom: 'var(--space-sm)' }}>
                Content-Addressed Hash (IPFS-style):
              </p>
              <div style={{ display: 'flex', gap: 'var(--space-md)' }}>
                <code style={{ flex: 1, wordBreak: 'break-all' }}>{shareModal.hash}</code>
                <Button
                  size="sm"
                  variant="secondary"
                  onClick={() => copyToClipboard(shareModal.hash)}
                >
                  Copy
                </Button>
              </div>
            </div>

            <div style={{ background: 'var(--color-bg-secondary)', padding: 'var(--space-lg)', borderRadius: 'var(--radius-md)', marginBottom: 'var(--space-lg)' }}>
              <p className="text-small" style={{ color: 'var(--color-text-secondary)', marginBottom: 'var(--space-sm)' }}>
                Share Link (simulated):
              </p>
              <div style={{ display: 'flex', gap: 'var(--space-md)' }}>
                <code style={{ flex: 1, wordBreak: 'break-all' }}>{`secureshare://share/${shareModal.hash}`}</code>
                <Button
                  size="sm"
                  variant="secondary"
                  onClick={() => copyToClipboard(`secureshare://share/${shareModal.hash}`)}
                >
                  Copy
                </Button>
              </div>
            </div>

            <p className="text-small" style={{ marginBottom: 'var(--space-lg)' }}>
              Share this hash with others to grant them access to your file. The content-addressed approach ensures security and data integrity.
            </p>

            <Button
              fullWidth
              variant="secondary"
              onClick={() => setShareModal(null)}
            >
              Close
            </Button>
          </Card>
        </div>
      )}
    </div>
  );
};

export default MyFiles;
