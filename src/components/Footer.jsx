import React from 'react';

/**
 * Footer Component - App footer with links and info
 */
const Footer = () => {
  return (
    <footer style={{ borderTop: '1px solid var(--color-border)', marginTop: 'var(--space-3xl)', padding: 'var(--space-2xl) 0' }}>
      <div className="container">
        <div className="grid-cols-3">
          <div>
            <h4 style={{ marginBottom: 'var(--space-md)' }}>SecureShare</h4>
            <p className="text-small">
              Decentralized AI-based file sharing platform for secure, private, and intelligent file management.
            </p>
          </div>
          <div>
            <h4 style={{ marginBottom: 'var(--space-md)' }}>Quick Links</h4>
            <ul style={{ listStyle: 'none', margin: 0, padding: 0 }}>
              <li style={{ marginBottom: 'var(--space-sm)' }}>
                <a href="/">Home</a>
              </li>
              <li style={{ marginBottom: 'var(--space-sm)' }}>
                <a href="/privacy">Privacy Policy</a>
              </li>
              <li style={{ marginBottom: 'var(--space-sm)' }}>
                <a href="/terms">Terms of Service</a>
              </li>
            </ul>
          </div>
          <div>
            <h4 style={{ marginBottom: 'var(--space-md)' }}>Contact</h4>
            <p className="text-small">Email: hello@secureshare.io</p>
            <p className="text-small">Built with ❤️ for privacy</p>
          </div>
        </div>
        <div style={{ marginTop: 'var(--space-2xl)', paddingTop: 'var(--space-lg)', borderTop: '1px solid var(--color-border)', textAlign: 'center' }}>
          <p className="text-small" style={{ color: 'var(--color-text-tertiary)' }}>
            © {new Date().getFullYear()} SecureShare. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
