import React, { useState } from 'react';
import Card from '../components/Card';
import Button from '../components/Button';
import Alert from '../components/Alert';
import { validateFile, generateAILabel, formatFileSize } from '../services/fileService';
import { addFile } from '../services/storageService';

/**
 * File Upload Page
 */
const FileUpload = () => {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [alerts, setAlerts] = useState([]);

  const addAlert = (type, title, message) => {
    const id = Date.now();
    setAlerts((prev) => [...prev, { id, type, title, message }]);
    setTimeout(() => {
      setAlerts((prev) => prev.filter((a) => a.id !== id));
    }, 5000);
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      processFile(files[0]);
    }
  };

  const handleFileSelect = (e) => {
    const files = e.target.files;
    if (files.length > 0) {
      processFile(files[0]);
    }
  };

  const processFile = (file) => {
    const validation = validateFile(file);

    if (!validation.valid) {
      addAlert('danger', 'Invalid File', validation.error);
      return;
    }

    setSelectedFile(file);

    // Show preview for images
    if (file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreview(e.target.result);
      };
      reader.readAsDataURL(file);
    } else {
      setPreview(null);
    }

    addAlert('success', 'File Selected', `${file.name} is ready to upload`);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      addAlert('warning', 'No File', 'Please select a file to upload');
      return;
    }

    setUploading(true);
    try {
      // Generate AI label
      const aiLabel = generateAILabel(selectedFile);

      // Create file metadata
      const fileMetadata = {
        name: selectedFile.name,
        size: selectedFile.size,
        type: selectedFile.type,
        aiLabel
      };

      // Add file to storage
      const result = addFile(fileMetadata);

      addAlert('success', 'Upload Complete', `${selectedFile.name} has been uploaded successfully!`);

      // Reset form
      setSelectedFile(null);
      setPreview(null);

      // Redirect after delay
      setTimeout(() => {
        window.location.href = '/my-files';
      }, 2000);
    } catch (error) {
      addAlert('danger', 'Upload Failed', error.message);
    } finally {
      setUploading(false);
    }
  };

  const handleClear = () => {
    setSelectedFile(null);
    setPreview(null);
  };

  return (
    <div className="container">
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        <h1 style={{ marginBottom: 'var(--space-lg)' }}>Upload Files</h1>

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

        {/* Upload Area */}
        <Card>
          <div
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            style={{
              border: '2px dashed',
              borderColor: dragActive ? 'var(--color-primary)' : 'var(--color-border)',
              borderRadius: 'var(--radius-lg)',
              padding: 'var(--space-2xl)',
              textAlign: 'center',
              backgroundColor: dragActive ? 'rgba(99, 102, 241, 0.05)' : 'var(--color-bg-secondary)',
              transition: 'all var(--transition-fast)',
              cursor: 'pointer'
            }}
          >
            <div style={{ fontSize: '48px', marginBottom: 'var(--space-md)' }}>📤</div>
            <h3 style={{ marginBottom: 'var(--space-sm)' }}>Drag & Drop Your Files Here</h3>
            <p className="text-small" style={{ marginBottom: 'var(--space-lg)' }}>
              or click the button below to select files from your computer
            </p>

            <input
              type="file"
              id="file-input"
              onChange={handleFileSelect}
              style={{ display: 'none' }}
              accept="image/*,.pdf,.txt,.doc,.docx,.xls,.xlsx,.zip,.mp4,.mp3"
            />

            <Button
              variant="primary"
              onClick={() => document.getElementById('file-input').click()}
              disabled={uploading}
            >
              Select File
            </Button>

            <p className="text-small" style={{ marginTop: 'var(--space-md)', color: 'var(--color-text-tertiary)' }}>
              Supported: Images, PDF, Documents, Spreadsheets, Archives, Videos (Max 100 MB)
            </p>
          </div>
        </Card>

        {/* File Preview */}
        {selectedFile && (
          <Card style={{ marginTop: 'var(--space-lg)' }}>
            <h3 style={{ marginBottom: 'var(--space-lg)' }}>File Preview</h3>

            {preview && (
              <div style={{ marginBottom: 'var(--space-lg)' }}>
                <img
                  src={preview}
                  alt="Preview"
                  style={{
                    maxWidth: '100%',
                    maxHeight: '300px',
                    borderRadius: 'var(--radius-lg)',
                    marginBottom: 'var(--space-md)'
                  }}
                />
              </div>
            )}

            <div style={{ background: 'var(--color-bg-secondary)', padding: 'var(--space-lg)', borderRadius: 'var(--radius-md)', marginBottom: 'var(--space-lg)' }}>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 'var(--space-md)' }}>
                <div>
                  <p className="text-small" style={{ color: 'var(--color-text-secondary)' }}>File Name</p>
                  <p className="font-bold">{selectedFile.name}</p>
                </div>
                <div>
                  <p className="text-small" style={{ color: 'var(--color-text-secondary)' }}>File Size</p>
                  <p className="font-bold">{formatFileSize(selectedFile.size)}</p>
                </div>
                <div>
                  <p className="text-small" style={{ color: 'var(--color-text-secondary)' }}>File Type</p>
                  <p className="font-bold">{selectedFile.type || 'Unknown'}</p>
                </div>
                <div>
                  <p className="text-small" style={{ color: 'var(--color-text-secondary)' }}>AI Label</p>
                  <p className="font-bold">{generateAILabel(selectedFile)}</p>
                </div>
              </div>
            </div>

            <div style={{ display: 'flex', gap: 'var(--space-md)' }}>
              <Button
                variant="primary"
                fullWidth
                loading={uploading}
                disabled={uploading}
                onClick={handleUpload}
              >
                {uploading ? 'Uploading...' : 'Upload File'}
              </Button>
              <Button
                variant="secondary"
                fullWidth
                disabled={uploading}
                onClick={handleClear}
              >
                Clear
              </Button>
            </div>
          </Card>
        )}

        {/* Info Section */}
        <Card style={{ marginTop: 'var(--space-lg)' }}>
          <h3 style={{ marginBottom: 'var(--space-md)' }}>How It Works</h3>
          <ol style={{ marginLeft: 'var(--space-lg)' }}>
            <li style={{ marginBottom: 'var(--space-md)' }}>
              <strong>Upload:</strong> Select or drag & drop your file. It will be validated for security.
            </li>
            <li style={{ marginBottom: 'var(--space-md)' }}>
              <strong>AI Processing:</strong> The file is automatically labeled and categorized using AI.
            </li>
            <li style={{ marginBottom: 'var(--space-md)' }}>
              <strong>Storage:</strong> File metadata is stored with a content-addressed hash (simulating IPFS).
            </li>
            <li>
              <strong>Access:</strong> Your files appear in "My Files" with instant access via secure hashes.
            </li>
          </ol>
        </Card>
      </div>
    </div>
  );
};

export default FileUpload;
