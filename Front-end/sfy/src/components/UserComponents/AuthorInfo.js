import React, { useState, useEffect, useRef } from 'react';
import { getDownloadURL, ref, uploadBytes } from 'firebase/storage';
import { storage } from '../../firebase';
import api from '../../axiosConfig';
import AuthorEditForm from './AuthorEditForm';
import './AuthorInfo.css';

const AuthorInfo = ({ user }) => {
  const [profilePictureUrl, setProfilePictureUrl] = useState('');
  const [isFollowing, setIsFollowing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [userFollowers, setUserFollowers] = useState(user.followers.length);
  const [isEditingPicture, setIsEditingPicture] = useState(false);
  const [isEditingInfo, setIsEditingInfo] = useState(false);
  const fileInputRef = useRef(null);

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
  }, [loggedInUserId, user.followers, profilePictureUrl]);

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

  const handlePictureChange = async (event) => {
    const file = event.target.files[0];
    if (file) {
      const formData = new FormData();
      formData.append('picture', file);

      try {
        const response = await api.post(`/user/upload_picture/`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        const url = response.data.picture_url;
        setProfilePictureUrl(url);
        setIsEditingPicture(false);
      } catch (error) {
        console.error('Error uploading picture:', error);
      }
    }
  };

  const fullName = user.first_name && user.last_name ? `${user.first_name} ${user.last_name}` :
    user.first_name || user.last_name || 'Name is hidden';

  return (
    <div className="author-info">
      <div
        className={`author-image-container ${loggedInUserId === user.id.toString() ? 'editable' : ''}`}
        onClick={() => loggedInUserId === user.id.toString() && fileInputRef.current.click()}
        onMouseEnter={() => loggedInUserId === user.id.toString() && setIsEditingPicture(true)}
        onMouseLeave={() => loggedInUserId === user.id.toString() && setIsEditingPicture(false)}
      >
        <img
          src={profilePictureUrl}
          alt="Profile"
          className="profile-picture"
        />
        {isEditingPicture && <div className="edit-overlay">Edit</div>}
        <input
          type="file"
          ref={fileInputRef}
          style={{ display: 'none' }}
          onChange={handlePictureChange}
        />
      </div>
      <div className="author-details">
        <h2>{user.username}</h2>
        <p>{fullName}</p>
        <p>Followers: {userFollowers}</p>
        {user.is_author && user.description && (
          <p className="description">{user.description}</p>
        )}
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
        {loggedInUserId === user.id.toString() && (
          <button onClick={() => setIsEditingInfo(!isEditingInfo)} className="edit-info-button-author">
            {isEditingInfo ? 'Cancel' : 'Edit Info'}
          </button>
        )}
        {isEditingInfo && (
          <AuthorEditForm user={user} onClose={() => setIsEditingInfo(false)} />
        )}
      </div>
    </div>
  );
};

export default AuthorInfo
