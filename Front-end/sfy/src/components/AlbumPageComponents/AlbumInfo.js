import React, { useState, useEffect, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getDownloadURL, ref } from 'firebase/storage';
import { storage } from '../../firebase';
import api from '../../axiosConfig';
import './AlbumInfo.css';
import AddSongForm from './AddSongForm';

const AlbumInfo = () => {
  const { id } = useParams();
  const [album, setAlbum] = useState(null);
  const [pictureUrl, setPictureUrl] = useState('');
  const [isFollowing, setIsFollowing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [showAddSongForm, setShowAddSongForm] = useState(false);
  const [albumFollowers, setAlbumFollowers] = useState(0);
  const [isEditingPicture, setIsEditingPicture] = useState(false);
  const fileInputRef = useRef(null);

  const loggedInUserId = localStorage.getItem('user_id');

  useEffect(() => {
    const fetchAlbum = async () => {
      try {
        const response = await api.get(`/album/get/${id}/`);
        setAlbum(response.data);
        setAlbumFollowers(response.data.followers.length);

        if (response.data.picture_url) {
          const storageRef = ref(storage, response.data.picture_url);
          const url = await getDownloadURL(storageRef);
          setPictureUrl(url);
        }

        if (loggedInUserId && response.data.followers.includes(parseInt(loggedInUserId, 10))) {
          setIsFollowing(true);
        }
      } catch (error) {
        console.error('Error fetching album:', error);
      }
    };

    fetchAlbum();
  }, [id, loggedInUserId]);

  const handleFollow = async () => {
    setLoading(true);
    try {
      await api.post(`/album/${id}/follow/`);
      setIsFollowing(true);
      setAlbumFollowers(prevFollowers => prevFollowers + 1);
    } catch (error) {
      console.error('Error following album:', error);
    }
    setLoading(false);
  };

  const handleUnfollow = async () => {
    setLoading(true);
    try {
      await api.delete(`/album/${id}/unfollow/`);
      setIsFollowing(false);
      setAlbumFollowers(prevFollowers => prevFollowers - 1);
    } catch (error) {
      console.error('Error unfollowing album:', error);
    }
    setLoading(false);
  };

  const handleAddSongClick = () => {
    setShowAddSongForm(true);
  };

  const handleCloseForm = () => {
    setShowAddSongForm(false);
  };

  const handlePictureChange = async (event) => {
    const file = event.target.files[0];
    if (file) {
      const formData = new FormData();
      formData.append('picture', file);

      try {
        const response = await api.patch(`/album/upload_picture/${id}/`, formData, {
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

  if (!album) {
    return <p>Loading...</p>;
  }

  const { title, owner_username, owner_id, songs } = album;
  const userId = parseInt(loggedInUserId, 10);

  return (
    <div className="album-info">
      <div
        className={`album-picture-container ${userId === owner_id ? 'editable' : ''}`}
        onClick={() => userId === owner_id && fileInputRef.current.click()}
        onMouseEnter={() => userId === owner_id && setIsEditingPicture(true)}
        onMouseLeave={() => userId === owner_id && setIsEditingPicture(false)}
      >
        <img src={pictureUrl} alt={title} className="album-picture" />
        {isEditingPicture && <div className="edit-overlay">Edit</div>}
        <input
          type="file"
          ref={fileInputRef}
          style={{ display: 'none' }}
          onChange={handlePictureChange}
        />
      </div>
      <div className="album-details">
        <h1>{title}</h1>
        <p>
          Author: <Link to={`/user/${owner_id}`}>{owner_username}</Link>
        </p>
        <p>{songs.length} Songs</p>
        <p>Followers: {albumFollowers}</p>
        {loggedInUserId && (
          <>
            {userId !== owner_id ? (
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
            ) : (
              <button onClick={handleAddSongClick}>Add Songs</button>
            )}
          </>
        )}
      </div>
      {showAddSongForm && <AddSongForm albumId={id} onClose={handleCloseForm} />}
    </div>
  );
};

export default AlbumInfo;
