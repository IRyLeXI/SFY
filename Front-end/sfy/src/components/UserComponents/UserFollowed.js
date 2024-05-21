import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../axiosConfig';
import FollowedUserCard from '../CardComponents/FollowedUserCard';
import './UserFollowed.css';

const UserFollowed = ({ userId }) => {
  const [followedUsers, setFollowedUsers] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchFollowedUsers = async () => {
      try {
        const response = await api.get(`/user/get/${userId}/followed/`);
        setFollowedUsers(response.data);
      } catch (error) {
        console.error('Error fetching followed users:', error);
      }
    };

    fetchFollowedUsers();
  }, [userId]);

  const handleUserClick = (id) => {
    navigate(`/user/${id}`);
  };

  return (
    <div className="user-followed">
      <h3>Followed Users</h3>
      <div className="followed-users-container">
        {followedUsers.map(user => (
          <FollowedUserCard key={user.id} user={user} onClick={() => handleUserClick(user.id)} />
        ))}
      </div>
    </div>
  );
};

export default UserFollowed;
