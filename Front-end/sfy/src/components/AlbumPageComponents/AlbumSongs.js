import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../../axiosConfig';
import SongCard from '../UserComponents/CardComponents/SongCard';
import './AlbumSongs.css';

const AlbumSongs = () => {
  const { id } = useParams();
  const [songs, setSongs] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSongs = async () => {
      try {
        const response = await api.get(`/album/${id}/songs/`);
        setSongs(response.data);
        localStorage.setItem('songQueue', JSON.stringify(response.data));
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching songs:', error);
        setError('Error fetching songs. Please try again later.');
        setIsLoading(false);
      }
    };

    fetchSongs();
  }, [id]);

  if (isLoading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <div className="album-page-songs">
      <div className="album-songs-header">
        <span>Song</span>
        <span>Created</span>
        <span><i className="fas fa-clock"></i></span>
        <span><i className="fas fa-headphones-alt"></i></span>
      </div>
      {songs.map(song => (
        <SongCard key={song.id} song={song} />
      ))}
    </div>
  );
};

export default AlbumSongs;
