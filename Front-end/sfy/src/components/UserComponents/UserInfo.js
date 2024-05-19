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
        <p>Followers: {user.followers.length}</p>
      </div>
    </div>
  );
};

export default UserInfo;
