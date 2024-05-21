import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getDownloadURL, ref } from 'firebase/storage';
import { storage } from '../../firebase';
import api from '../../axiosConfig';
import './PlaylistInfo.css';

const PlaylistInfo = () => {
  const { id } = useParams();
  const [playlist, setPlaylist] = useState(null);
  const [pictureUrl, setPictureUrl] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchPlaylist = async () => {
      try {
        const response = await api.get(`/playlist/get/${id}/`);
        setPlaylist(response.data);
        setIsLoading(false);

        // Fetch the picture URL from Firebase
        const storageRef = ref(storage, response.data.picture_url);
        const url = await getDownloadURL(storageRef);
        setPictureUrl(url);
      } catch (error) {
        console.error('Error fetching playlist:', error);
        setIsLoading(false);
      }
    };

    fetchPlaylist();
  }, [id]);

  if (isLoading) {
    return <p>Loading...</p>;
  }

  if (!playlist) {
    return <p>Playlist not found</p>;
  }

  const { title, owner_username, owner_id, songs, followers, total_duration } = playlist;

  const formatDuration = (duration) => {
    const [hours, minutes, seconds] = duration.split(':');
    return `${hours} Hours, ${minutes} Minutes`;
  };

  return (
    <div className="playlist-info">
      <img src={pictureUrl} alt={title} className="playlist-picture" />
      <div className="playlist-details">
        <h1>{title}</h1>
        <p>
          Author: <Link to={`/user/${owner_id}`}>{owner_username}</Link>
        </p>
        <p>{songs.length} Songs, {formatDuration(total_duration)}</p>
        <p>{followers.length} Followers</p>
      </div>
    </div>
  );
};

export default PlaylistInfo;
