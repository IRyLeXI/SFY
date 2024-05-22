import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../axiosConfig';
import './RegisterPage.css';

const RegistrationPage = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    description: '',
    is_author: false,
  });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const userPayload = {
      ...formData,
      is_active: true,
    };

    const url = formData.is_author
      ? 'http://localhost:8000/api/author/create/'
      : 'http://localhost:8000/api/user/create/';

    try {
      const response = await api.post(url, userPayload);
      navigate('/login');
    } catch (error) {
      setError('Registration failed. Please check your input.');
      console.error('Registration error:', error);
    }
  };

  return (
    <div className="registration-page">
      <form onSubmit={handleSubmit}>
        <h2>Register</h2>
        {error && <div className="error">{error}</div>}
        <div>
          <label>Username*:</label>
          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Email*:</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Password*:</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>First Name:</label>
          <input
            type="text"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Last Name:</label>
          <input
            type="text"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>
            Author:
            <input
              type="checkbox"
              name="is_author"
              checked={formData.is_author}
              onChange={handleChange}
            />
          </label>
        </div>
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default RegistrationPage;
