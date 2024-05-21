import React, { useState, useEffect, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getDownloadURL, ref } from 'firebase/storage';
import { storage } from '../../firebase';
import api from '../../axiosConfig';
import './PlaylistInfo.css';

const PlaylistInfo = () => {
  const { id } = useParams();
  const [playlist, setPlaylist] = useState(null);
  const [pictureUrl, setPictureUrl] = useState('');
  const [isFollowing, setIsFollowing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [playlistFollowers, setPlaylistFollowers] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [isEditingPicture, setIsEditingPicture] = useState(false);
  const fileInputRef = useRef(null);

  const loggedInUserId = localStorage.getItem('user_id');

  useEffect(() => {
    const fetchPlaylist = async () => {
      try {
        const response = await api.get(`/playlist/get/${id}/`);
        setPlaylist(response.data);
        setPlaylistFollowers(response.data.followers.length);
        setIsLoading(false);

        const storageRef = ref(storage, response.data.picture_url);
        const url = await getDownloadURL(storageRef);
        setPictureUrl(url);

        if (loggedInUserId && response.data.followers.includes(parseInt(loggedInUserId, 10))) {
          setIsFollowing(true);
        }
      } catch (error) {
        console.error('Error fetching playlist:', error);
        setIsLoading(false);
      }
    };

    fetchPlaylist();
  }, [id, loggedInUserId, pictureUrl]);

  const handleFollow = async () => {
    setLoading(true);
    try {
      await api.post(`/playlist/${id}/follow/`);
      setIsFollowing(true);
      setPlaylistFollowers(prevFollowers => prevFollowers + 1);
    } catch (error) {
      console.error('Error following playlist:', error);
    }
    setLoading(false);
  };

  const handleUnfollow = async () => {
    setLoading(true);
    try {
      await api.delete(`/playlist/${id}/unfollow/`);
      setIsFollowing(false);
      setPlaylistFollowers(prevFollowers => prevFollowers - 1);
    } catch (error) {
      console.error('Error unfollowing playlist:', error);
    }
    setLoading(false);
  };

  const handlePictureChange = async (event) => {
    const file = event.target.files[0];
    if (file) {
      const formData = new FormData();
      formData.append('picture', file);

      try {
        const response = await api.patch(`/playlist/upload_picture/${id}/`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        const url = response.data.picture_url;
        setPictureUrl(url);
        setIsEditingPicture(false);
      } catch (error) {
        console.error('Error uploading picture:', error);
      }
    }
  };

  const { title, owner_username, owner_id, songs, total_duration } = playlist || {};
  const userId = parseInt(loggedInUserId, 10);

  const formatDuration = (duration) => {
    const [hours, minutes, seconds] = duration.split(':');
    return `${hours} Hours, ${minutes} Minutes`;
  };

  if (isLoading) {
    return <p>Loading...</p>;
  }

  if (!playlist) {
    return <p>Playlist not found</p>;
  }

  return (
    <div className="playlist-info">
      <div
        className={`playlist-picture-container ${userId === owner_id ? 'editable' : ''}`}
        onClick={() => userId === owner_id && fileInputRef.current.click()}
        onMouseEnter={() => userId === owner_id && setIsEditingPicture(true)}
        onMouseLeave={() => userId === owner_id && setIsEditingPicture(false)}
      >
        <img src={pictureUrl} alt={title} className="playlist-picture" />
        {isEditingPicture && <div className="edit-overlay">Edit</div>}
        <input
          type="file"
          ref={fileInputRef}
          style={{ display: 'none' }}
          onChange={handlePictureChange}
        />
      </div>
      <div className="playlist-details">
        <h1>{title}</h1>
        <p>
          Author: <Link to={`/user/${owner_id}`}>{owner_username}</Link>
        </p>
        <p>{songs.length} Songs, {formatDuration(total_duration)}</p>
        <p>Followers: {playlistFollowers}</p>
        {loggedInUserId && userId !== owner_id && (
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

export default PlaylistInfo;
