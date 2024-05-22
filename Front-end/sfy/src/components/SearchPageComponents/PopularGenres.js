import React, { useState, useEffect } from 'react';
import api from '../../axiosConfig';
import PlaylistCard from '../CardComponents/PlaylistCard';
import './PopularGenres.css';

const PopularGenres = () => {
  const [playlists, setPlaylists] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPlaylists = async () => {
      try {
        const response = await api.get('/playlist/get/global/');
        setPlaylists(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching popular genres:', error);
        setError('Error fetching popular genres');
        setLoading(false);
      }
    };

    fetchPlaylists();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="popular-genres">
      <h3>Popular Genres</h3>
      <div className="playlist-cards-container-search">
        {playlists.map((playlist) => (
          <PlaylistCard key={playlist.id} playlist={playlist} />
        ))}
      </div>
    </div>
  );
};

export default PopularGenres;
