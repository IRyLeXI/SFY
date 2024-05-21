import React from 'react';
import { getDownloadURL, ref } from 'firebase/storage';
import { useNavigate } from 'react-router-dom';
import { storage } from '../../firebase';
import './PlaylistCard.css';
import { useState, useEffect } from 'react';

const PlaylistCard = ({ playlist }) => {
  const [pictureUrl, setPictureUrl] = useState('');
  const navigate = useNavigate();

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


  const handleCardClick = () => {
    navigate(`/playlist/${playlist.id}`);
  };

  // console.log(playlist)
  return (
    <div className="playlist-card" onClick={handleCardClick}> 
      <img src={pictureUrl} alt="Playlist" className="playlist-card-picture" />
      <div className="playlist-card-info">
        <h4>{playlist.title}</h4>
        <p>Owner: {playlist.owner_username}</p>
        <p>Updated: {new Date(playlist.updated_date).toLocaleDateString()}</p>
      </div>
    </div>
  );
};

export default PlaylistCard;
