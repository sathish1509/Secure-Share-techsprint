import React from 'react';

/**
 * File Card Component - Displays file metadata with actions
 */
const FileCard = ({ file, onDelete, onPreview, onShare }) => {
  const getFileIcon = (type) => {
    if (type.includes('image')) return '🖼️';
    if (type.includes('pdf')) return '📄';
    if (type.includes('word') || type.includes('document')) return '📝';
    if (type.includes('sheet') || type.includes('excel')) return '📊';
    if (type.includes('video')) return '🎥';
    if (type.includes('audio')) return '🎵';
    if (type.includes('zip')) return '📦';
    return '📁';
  };

  const formatBytes = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  return (
    <div className="card">
      <div style={{ display: 'flex', gap: 'var(--space-md)' }}>
        <div style={{ fontSize: '32px' }}>{getFileIcon(file.type)}</div>
        <div style={{ flex: 1 }}>
          <h4 style={{ marginBottom: 'var(--space-xs)' }}>{file.name}</h4>
          <p className="text-small" style={{ marginBottom: 'var(--space-xs)' }}>
            {formatBytes(file.size)} • {formatDate(file.uploadedAt)}
          </p>
          <p className="text-small" style={{ color: 'var(--color-primary)' }}>
            {file.aiLabel}
          </p>
          <p className="text-small" style={{ color: 'var(--color-text-tertiary)', marginBottom: 'var(--space-md)' }}>
            Hash: {file.hash.substring(0, 12)}...
          </p>
        </div>
      </div>
      <div style={{ display: 'flex', gap: 'var(--space-sm)', justifyContent: 'flex-end', paddingTop: 'var(--space-md)', borderTop: '1px solid var(--color-border)' }}>
        {onPreview && (
          <button className="btn btn-secondary btn-small" onClick={() => onPreview(file)}>
            Preview
          </button>
        )}
        {onShare && (
          <button className="btn btn-secondary btn-small" onClick={() => onShare(file)}>
            Share
          </button>
        )}
        {onDelete && (
          <button className="btn btn-danger btn-small" onClick={() => onDelete(file.id)}>
            Delete
          </button>
        )}
      </div>
    </div>
  );
};

export default FileCard;
