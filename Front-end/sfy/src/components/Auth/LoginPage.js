import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';
import api from '../../axiosConfig';
import './LoginPage.css';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const checkAuth = async () => {
      const accessToken = localStorage.getItem('accessToken');
      const refreshToken = localStorage.getItem('refreshToken');

      if (accessToken && refreshToken) {
        try {
          const response = await api.get('/user/check/');
          if (response.status === 200) {
            const decodedToken = jwtDecode(accessToken);
            const userId = decodedToken.user_id;
            navigate(`/user/${userId}`);
            window.location.reload();
          }
        } catch (error) {
          console.error('Access token is invalid or expired:', error);
        }
      }
    };

    checkAuth();
  }, [navigate]);

  const handleLogin = async (event) => {
    event.preventDefault();
    try {
      const response = await api.post('/token/', {
        username,
        password,
      });
      const decodedToken = jwtDecode(response.data.access);
      const userId = decodedToken.user_id;

      localStorage.setItem('accessToken', response.data.access);
      localStorage.setItem('refreshToken', response.data.refresh);
      localStorage.setItem('user_id', userId);

      navigate(`/user/${userId}`);
      window.location.reload();
    } catch (error) {
      setError('Login failed. Please check your username and password.');
      console.error('Login error:', error);
    }
  };

  return (
    <div className="login-page">
      <form onSubmit={handleLogin}>
        <h2>Login</h2>
        {error && <div className="error">{error}</div>}
        <div>
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default LoginPage;
