import React from 'react';

/**
 * Alert Component - Displays messages and notifications
 */
const Alert = ({ type = 'info', title, message, onClose }) => {
  const alertClass = `alert alert-${type}`;

  return (
    <div className={alertClass}>
      <div style={{ flex: 1 }}>
        {title && <strong>{title}</strong>}
        {title && message && <br />}
        {message}
      </div>
      {onClose && (
        <button
          onClick={onClose}
          style={{
            background: 'none',
            border: 'none',
            cursor: 'pointer',
            fontSize: 'var(--font-size-lg)',
            color: 'inherit'
          }}
        >
          ✕
        </button>
      )}
    </div>
  );
};

export default Alert;
