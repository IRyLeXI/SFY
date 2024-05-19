import React from 'react';
import { getDownloadURL, ref } from 'firebase/storage';
import { storage } from '../../firebase';
import './PlaylistCard.css';
import { useState, useEffect } from 'react';

const PlaylistCard = ({ playlist }) => {
  const [pictureUrl, setPictureUrl] = useState('');

  useEffect(() => {
    const fetchPictureUrl = async () => {
      try {
        const storageRef = ref(storage, playlist.picture_url);
        const url = await getDownloadURL(storageRef);
        setPictureUrl(url);
      } catch (error) {
        console.error('Error fetching playlist picture:', error);
      }
    };

    fetchPictureUrl();
  }, [playlist.picture_url]);

  return (
    <div className="playlist-card">
      <img src={pictureUrl} alt="Playlist" className="playlist-picture" />
      <div className="playlist-info">
        <h4>{playlist.title}</h4>
        <p>Owner: {playlist.owner}</p>
        <p>Updated: {new Date(playlist.updated_date).toLocaleDateString()}</p>
      </div>
    </div>
  );
};

export default PlaylistCard;
