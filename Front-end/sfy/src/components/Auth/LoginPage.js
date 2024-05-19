import React, { useState } from 'react';
import api from '../../api';
import './LoginPage.css';

const LoginPage = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await api.post('token/', { username, password });
      const { access, refresh } = response.data;
      console.log(response.data)
      const decodedToken = JSON.parse(atob(access.split('.')[1]));
      const userId = decodedToken.user_id;

      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      localStorage.setItem('user_id', userId);

      onLogin(userId);
    } catch (error) {
      setError('Invalid username or password');
    }
  };

  return (
    <div className="login-page">
      <form onSubmit={handleLogin}>
        <h2>Login</h2>
        <div>
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        {error && <p className="error">{error}</p>}
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default LoginPage;
