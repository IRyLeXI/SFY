import React, { useState, useEffect } from 'react';
import { getDownloadURL, ref } from 'firebase/storage';
import { storage } from '../../firebase';
import './UserInfo.css';

const UserInfo = ({ user }) => {
  const [profilePictureUrl, setProfilePictureUrl] = useState('');

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

  return (
    <div className="user-info">
      {profilePictureUrl ? (
        <img src={profilePictureUrl} alt="Profile" className="profile-picture" />
      ) : (
        <img src="default-profile-picture-url" alt="Profile" className="profile-picture" />
      )}
      <h2>{user.username}</h2>
      <p>Followers: {user.followers_count}</p>
      {/* Додати іншу інформацію, якщо потрібно */}
    </div>
  );
};

export default UserInfo;
