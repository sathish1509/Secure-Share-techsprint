import React from 'react';

/**
 * Input Component - Reusable form input with label and error handling
 */
const Input = ({
  label,
  type = 'text',
  name,
  value,
  onChange,
  placeholder,
  required = false,
  error,
  success,
  disabled = false,
  ...props
}) => {
  return (
    <div className="form-group">
      {label && (
        <label className="form-label">
          {label}
          {required && <span className="form-required">*</span>}
        </label>
      )}
      <input
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className="form-input"
        disabled={disabled}
        {...props}
      />
      {error && <span className="form-error">{error}</span>}
      {success && <span className="form-success">{success}</span>}
    </div>
  );
};

export default Input;
