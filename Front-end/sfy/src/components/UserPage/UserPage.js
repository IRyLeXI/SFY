import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../../axiosConfig';
import UserInfo from '../UserComponents/UserInfo';
import UserPlaylists from '../UserComponents/UserPlaylists';
import UserFollowed from '../UserComponents/UserFollowed';
import './UserPage.css';

const UserPage = () => {
  const { id } = useParams();
  const [user, setUser] = useState(null);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await api.get(`/user/get/${id}/`);
        setUser(response.data);
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    };

    fetchUserData();
  }, [id]);

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <div className="user-page">
      <UserInfo user={user} />
      <UserPlaylists userId={id} />
      <UserFollowed userId={id} />
    </div>
  );
};

export default UserPage;
