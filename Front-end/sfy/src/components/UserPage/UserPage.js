import React, { useState, useEffect } from 'react';
import UserInfo from '../UserComponents/UserInfo';
import api from '../../api';
import './UserPage.css';

const UserPage = () => {
  const [user, setUser] = useState(null);
  const userId = localStorage.getItem('user_id');

  useEffect(() => {
    if (userId) {
      api.get(`user/get/${userId}/`)
        .then(response => setUser(response.data))
        .catch(error => console.error('Error fetching user data:', error));
    }
  }, [userId]);

  if (!userId) {
    return <div>Please log in to see user information.</div>;
  }

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <div className="user-page">
      <UserInfo user={user} />
      {/* Додати інші компоненти для відображення плейлистів, підписок тощо */}
    </div>
  );
};

export default UserPage;