import React, { useState, useEffect } from 'react';
import api from '../../axiosConfig';
import AlbumCard from '../CardComponents/AlbumCard';
import './RecommendedAlbums.css';

const RecommendedAlbums = () => {
  const [albums, setAlbums] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchRecommendedAlbums = async () => {
      try {
        const response = await api.get('/album/recommended/');
        setAlbums(response.data);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching recommended albums:', error);
        setIsLoading(false);
      }
    };

    fetchRecommendedAlbums();
  }, []);

  return (
    <div className="recommended-albums">
      <h2>Recommended Albums</h2>
      <div className="album-cards-container">
        {isLoading ? (
          <p>Loading...</p>
        ) : (
          albums.map((album) => (
            <AlbumCard key={album.id} album={album} />
          ))
        )}
      </div>
    </div>
  );
};

export default RecommendedAlbums;
