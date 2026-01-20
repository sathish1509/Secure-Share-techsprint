import React, { useState, useEffect } from 'react';
import Card from '../components/Card';
import Button from '../components/Button';
import { getUserProfile } from '../services/storageService';
import { getRandomColor, formatDate } from '../utils/helpers';

/**
 * Dashboard Page - User profile and overview
 */
const Dashboard = ({ user }) => {
  const [profile, setProfile] = useState(null);
  const [stats, setStats] = useState({
    totalFiles: 0,
    storageUsed: 0,
    storageQuota: 10 * 1024 * 1024 * 1024 // 10 GB
  });

  useEffect(() => {
    const profile = getUserProfile();
    setProfile(profile);

    // Calculate stats
    const filesData = JSON.parse(localStorage.getItem('secureshare_files') || '[]');
    const totalSize = filesData.reduce((sum, file) => sum + file.size, 0);

    setStats({
      totalFiles: filesData.length,
      storageUsed: totalSize,
      storageQuota: profile?.storageQuota || 10 * 1024 * 1024 * 1024
    });
  }, []);

  const formatBytes = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
  };

  const storagePercentage = (stats.storageUsed / stats.storageQuota) * 100;

  return (
    <div className="container">
      <div style={{ marginBottom: 'var(--space-2xl)' }}>
        <h1 style={{ marginBottom: 'var(--space-lg)' }}>Dashboard</h1>
      </div>

      {/* Profile Section */}
      <div className="grid-cols-2" style={{ marginBottom: 'var(--space-2xl)' }}>
        <Card>
          <div style={{ display: 'flex', gap: 'var(--space-lg)', alignItems: 'center' }}>
            <div style={{
              width: '80px',
              height: '80px',
              borderRadius: '50%',
              background: getRandomColor(profile?.email),
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
              fontSize: '32px',
              fontWeight: 'bold'
            }}>
              {profile?.name?.charAt(0)?.toUpperCase()}
            </div>
            <div>
              <h2 style={{ marginBottom: 'var(--space-sm)' }}>{profile?.name}</h2>
              <p className="text-small">{profile?.email}</p>
              <p className="text-small" style={{ color: 'var(--color-text-tertiary)' }}>
                Member since {formatDate(profile?.createdAt)}
              </p>
            </div>
          </div>
        </Card>

        <Card>
          <div>
            <h3 style={{ marginBottom: 'var(--space-lg)' }}>Quick Actions</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-md)' }}>
              <a href="/upload" className="btn btn-primary" style={{ textAlign: 'center' }}>
                📤 Upload New File
              </a>
              <a href="/my-files" className="btn btn-secondary" style={{ textAlign: 'center' }}>
                📁 View All Files
              </a>
            </div>
          </div>
        </Card>
      </div>

      {/* Storage Stats */}
      <div className="grid-cols-3" style={{ marginBottom: 'var(--space-2xl)' }}>
        <Card>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '32px', marginBottom: 'var(--space-md)' }}>📁</div>
            <h4>Total Files</h4>
            <p style={{ fontSize: 'var(--font-size-2xl)', fontWeight: 'bold', color: 'var(--color-primary)', marginTop: 'var(--space-md)' }}>
              {stats.totalFiles}
            </p>
          </div>
        </Card>

        <Card>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '32px', marginBottom: 'var(--space-md)' }}>💾</div>
            <h4>Storage Used</h4>
            <p style={{ fontSize: 'var(--font-size-2xl)', fontWeight: 'bold', color: 'var(--color-primary)', marginTop: 'var(--space-md)' }}>
              {formatBytes(stats.storageUsed)}
            </p>
          </div>
        </Card>

        <Card>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '32px', marginBottom: 'var(--space-md)' }}>🔐</div>
            <h4>Storage Quota</h4>
            <p style={{ fontSize: 'var(--font-size-2xl)', fontWeight: 'bold', color: 'var(--color-primary)', marginTop: 'var(--space-md)' }}>
              {formatBytes(stats.storageQuota)}
            </p>
          </div>
        </Card>
      </div>

      {/* Storage Bar */}
      <Card>
        <h3 style={{ marginBottom: 'var(--space-md)' }}>Storage Usage</h3>
        <div style={{
          height: '8px',
          background: 'var(--color-bg-secondary)',
          borderRadius: 'var(--radius-full)',
          overflow: 'hidden',
          marginBottom: 'var(--space-md)'
        }}>
          <div style={{
            height: '100%',
            width: `${Math.min(storagePercentage, 100)}%`,
            background: storagePercentage > 80 ? 'var(--color-danger)' : 'var(--color-primary)',
            transition: 'width 0.3s ease'
          }} />
        </div>
        <p className="text-small">
          {formatBytes(stats.storageUsed)} of {formatBytes(stats.storageQuota)} used ({storagePercentage.toFixed(1)}%)
        </p>
      </Card>

      {/* Features Section */}
      <div style={{ marginTop: 'var(--space-2xl)' }}>
        <h2 style={{ marginBottom: 'var(--space-lg)' }}>Platform Features</h2>
        <div className="grid-cols-2">
          <Card>
            <div style={{ display: 'flex', gap: 'var(--space-md)' }}>
              <div style={{ fontSize: '24px' }}>🔒</div>
              <div>
                <h4>End-to-End Encrypted</h4>
                <p className="text-small">All your files are encrypted with military-grade security.</p>
              </div>
            </div>
          </Card>

          <Card>
            <div style={{ display: 'flex', gap: 'var(--space-md)' }}>
              <div style={{ fontSize: '24px' }}>🤖</div>
              <div>
                <h4>AI-Powered Labels</h4>
                <p className="text-small">Automatic intelligent categorization of your files.</p>
              </div>
            </div>
          </Card>

          <Card>
            <div style={{ display: 'flex', gap: 'var(--space-md)' }}>
              <div style={{ fontSize: '24px' }}>⛓️</div>
              <div>
                <h4>Decentralized Storage</h4>
                <p className="text-small">Content-addressed storage via IPFS for true decentralization.</p>
              </div>
            </div>
          </Card>

          <Card>
            <div style={{ display: 'flex', gap: 'var(--space-md)' }}>
              <div style={{ fontSize: '24px' }}>🌍</div>
              <div>
                <h4>Privacy First</h4>
                <p className="text-small">Your data stays private. We never access your files.</p>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
