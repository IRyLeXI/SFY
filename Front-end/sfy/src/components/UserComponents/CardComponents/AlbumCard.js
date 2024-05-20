import React, { useState, useEffect } from 'react';
import { getDownloadURL, ref } from 'firebase/storage';
import { storage } from '../../../firebase';
import './AlbumCard.css';

const AlbumCard = ({ album }) => {
  const [pictureUrl, setPictureUrl] = useState('');

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
  console.log(album)
  return (
    <div className="album-card">
      <img src={pictureUrl} alt="Album" className="album-picture" />
      <div className="album-info">
        <h4>{album.title}</h4>
        <p>Owner: {album.owner_username}</p>
        <p>Published: {new Date(album.publish_date).toLocaleDateString()}</p>
        <p>Genre: {album.major_genre}</p>
      </div>
    </div>
  );
};

export default AlbumCard;
