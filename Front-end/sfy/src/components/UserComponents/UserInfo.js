import React, { useState, useEffect } from 'react';
import { getDownloadURL, ref } from 'firebase/storage';
import { storage } from '../../firebase';
import axios from '../../axiosConfig';
import './UserInfo.css';
import api from '../../axiosConfig';

const UserInfo = ({ user }) => {
  const [profilePictureUrl, setProfilePictureUrl] = useState('');
  const [isFollowing, setIsFollowing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [userFollowers, setUserFollowers] = useState(user.followers.length)

  const loggedInUserId = localStorage.getItem('user_id');

  useEffect(() => {
    const fetchProfilePicture = async () => {
      if (user.picture_url) {
        try {
          const storageRef = ref(storage, user.picture_url);
          const url = await getDownloadURL(storageRef);
          setProfilePictureUrl(url);
        } catch (error) {
          console.error('Error fetching profile picture:', error);
        }
      }
    };

    fetchProfilePicture();
  }, [user.picture_url]);

  useEffect(() => {
    if (loggedInUserId && user.followers.includes(parseInt(loggedInUserId, 10))) {
      setIsFollowing(true);
    }
  }, [loggedInUserId, user.followers]);

  const handleFollow = async () => {
    setLoading(true);
    try {
      await api.post(`/user/follow/${user.id}/`);
      setIsFollowing(true);
      setUserFollowers(prevFollowers => prevFollowers + 1);
    } catch (error) {
      console.error('Error following user:', error);
    }
    setLoading(false);
  };

  const handleUnfollow = async () => {
    setLoading(true);
    try {
      await api.delete(`/user/unfollow/${user.id}/`);
      setIsFollowing(false);
      setUserFollowers(prevFollowers => prevFollowers - 1);
    } catch (error) {
      console.error('Error unfollowing user:', error);
    }
    setLoading(false);
  };

  const fullName = user.first_name && user.last_name ? `${user.first_name} ${user.last_name}` :
    user.first_name || user.last_name || 'Name is hidden';

  return (
    <div className="user-info">
      <div className='user-image-container'>
        <img
          src={profilePictureUrl || "default-profile-picture-url"}
          alt="Profile"
          className="profile-picture"
        />
      </div>
      <div className="user-details">
        <h2>{user.username}</h2>
        <p>{fullName}</p>
        <p>Followers: {userFollowers}</p>
        {loggedInUserId && loggedInUserId !== user.id.toString() && (
          <div>
            {isFollowing ? (
              <button onClick={handleUnfollow} disabled={loading}>
                Unfollow
              </button>
            ) : (
              <button onClick={handleFollow} disabled={loading}>
                Follow
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default UserInfo;
