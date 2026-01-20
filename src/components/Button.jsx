import React from 'react';

/**
 * Button Component - Reusable button with multiple variants
 */
const Button = ({
  children,
  onClick,
  type = 'button',
  variant = 'primary',
  size = 'md',
  fullWidth = false,
  disabled = false,
  loading = false,
  ...props
}) => {
  const variantClass = `btn-${variant}`;
  const sizeClass = size === 'sm' ? 'btn-small' : '';
  const blockClass = fullWidth ? 'btn-block' : '';
  const loadingClass = loading ? 'btn-loading' : '';

  return (
    <button
      type={type}
      className={`btn ${variantClass} ${sizeClass} ${blockClass} ${loadingClass}`}
      onClick={onClick}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? <span className="spinner"></span> : null}
      {children}
    </button>
  );
};

export default Button;
