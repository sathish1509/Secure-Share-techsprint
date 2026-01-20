import React from 'react';

/**
 * Card Component - Reusable container for content
 */
const Card = ({ children, title, subtitle, footer, clickable = false, ...props }) => {
  return (
    <div className={`card ${clickable ? 'cursor-pointer' : ''}`} {...props}>
      {title && <h3>{title}</h3>}
      {subtitle && <p className="text-muted">{subtitle}</p>}
      <div>{children}</div>
      {footer && <div style={{ marginTop: 'var(--space-md)', paddingTop: 'var(--space-md)', borderTop: '1px solid var(--color-border)' }}>{footer}</div>}
    </div>
  );
};

export default Card;
