import React, { useState, useEffect,  } from 'react';
import { getDownloadURL, ref } from 'firebase/storage';
import { storage } from '../../firebase';
import './AlbumCard.css';
import { useNavigate } from 'react-router-dom';

const AlbumCard = ({ album }) => {
  const [pictureUrl, setPictureUrl] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPictureUrl = async () => {
      try {
        const storageRef = ref(storage, album.picture_url);
        const url = await getDownloadURL(storageRef);
        setPictureUrl(url);
      } catch (error) {
        console.error('Error fetching album picture:', error);
      }
    };

    fetchPictureUrl();
  }, [album.picture_url]);

  const handleAlbumClick = () => {
    navigate(`/album/${album.id}`);
  };


  return (
    <div className="album-card" onClick={handleAlbumClick}>
      <img src={pictureUrl} alt="Album" className="album-card-picture" />
      <div className="album-card-info">
        <h4>{album.title}</h4>
        <p>Owner: {album.owner_username}</p>
        <p>Published: {new Date(album.publish_date).toLocaleDateString()}</p>
        <p>Genre: {album.genre_name}</p>
      </div>
    </div>
  );
};

export default AlbumCard;
