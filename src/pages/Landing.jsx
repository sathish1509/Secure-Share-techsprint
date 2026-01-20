import React from 'react';
import Card from '../components/Card';
import Button from '../components/Button';

/**
 * Landing Page - Homepage with features and CTAs
 */
const Landing = ({ user }) => {
  return (
    <div>
      {/* Hero Section */}
      <section style={{
        background: 'linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%)',
        color: 'white',
        padding: 'var(--space-3xl) 0',
        textAlign: 'center'
      }}>
        <div className="container">
          <div style={{ maxWidth: '800px', margin: '0 auto' }}>
            <h1 style={{ fontSize: 'var(--font-size-3xl)', marginBottom: 'var(--space-lg)', color: 'white' }}>
              🔐 SecureShare
            </h1>
            <p style={{ fontSize: 'var(--font-size-xl)', marginBottom: 'var(--space-lg)', opacity: 0.95 }}>
              Decentralized, AI-powered file sharing platform for secure and private collaboration
            </p>
            <div style={{ display: 'flex', gap: 'var(--space-md)', justifyContent: 'center', flexWrap: 'wrap' }}>
              {user ? (
                <>
                  <Button variant="primary" onClick={() => window.location.href = '/upload'}>
                    Upload Files
                  </Button>
                  <Button variant="primary" onClick={() => window.location.href = '/my-files'}>
                    View My Files
                  </Button>
                </>
              ) : (
                <>
                  <a href="/signup" className="btn btn-primary">
                    Get Started Free
                  </a>
                  <a href="/login" className="btn btn-secondary" style={{ color: 'white', borderColor: 'rgba(255,255,255,0.3)' }}>
                    Sign In
                  </a>
                </>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section style={{ padding: 'var(--space-3xl) 0', backgroundColor: 'var(--color-bg-secondary)' }}>
        <div className="container">
          <h2 style={{ textAlign: 'center', marginBottom: 'var(--space-2xl)' }}>Why Choose SecureShare?</h2>
          <div className="grid-cols-3">
            <Card>
              <div style={{ fontSize: '48px', marginBottom: 'var(--space-md)' }}>🔒</div>
              <h3>End-to-End Encrypted</h3>
              <p>Your files are encrypted and only accessible by you and authorized recipients.</p>
            </Card>
            <Card>
              <div style={{ fontSize: '48px', marginBottom: 'var(--space-md)' }}>🤖</div>
              <h3>AI-Powered Organization</h3>
              <p>Automatic file labeling and categorization powered by privacy-safe AI models.</p>
            </Card>
            <Card>
              <div style={{ fontSize: '48px', marginBottom: 'var(--space-md)' }}>⛓️</div>
              <h3>Decentralized Storage</h3>
              <p>Content-addressed storage using IPFS for truly decentralized file management.</p>
            </Card>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section style={{ padding: 'var(--space-3xl) 0' }}>
        <div className="container">
          <h2 style={{ textAlign: 'center', marginBottom: 'var(--space-2xl)' }}>How It Works</h2>
          <div className="grid-cols-3">
            <div style={{ textAlign: 'center' }}>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: '60px',
                height: '60px',
                background: 'var(--color-primary)',
                color: 'white',
                borderRadius: '50%',
                margin: '0 auto var(--space-lg)',
                fontSize: '28px'
              }}>
                1
              </div>
              <h4>Upload Files</h4>
              <p>Drag and drop or select files from your computer to upload securely.</p>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: '60px',
                height: '60px',
                background: 'var(--color-primary)',
                color: 'white',
                borderRadius: '50%',
                margin: '0 auto var(--space-lg)',
                fontSize: '28px'
              }}>
                2
              </div>
              <h4>Get AI Labels</h4>
              <p>Files are automatically labeled and categorized for easy organization.</p>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: '60px',
                height: '60px',
                background: 'var(--color-primary)',
                color: 'white',
                borderRadius: '50%',
                margin: '0 auto var(--space-lg)',
                fontSize: '28px'
              }}>
                3
              </div>
              <h4>Share Securely</h4>
              <p>Share files with recipients using content-addressed hashes via IPFS.</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section style={{
        background: 'var(--color-bg-secondary)',
        padding: 'var(--space-2xl) 0',
        textAlign: 'center'
      }}>
        <div className="container">
          <h2 style={{ marginBottom: 'var(--space-lg)' }}>Ready to secure your files?</h2>
          <p style={{ marginBottom: 'var(--space-lg)', fontSize: 'var(--font-size-lg)' }}>
            {user ? 'Start uploading files now.' : 'Join SecureShare for free today.'}
          </p>
          {!user && (
            <a href="/signup" className="btn btn-primary" style={{ fontSize: 'var(--font-size-lg)', padding: 'var(--space-md) var(--space-xl)' }}>
              Create Your Account
            </a>
          )}
        </div>
      </section>
    </div>
  );
};

export default Landing;
