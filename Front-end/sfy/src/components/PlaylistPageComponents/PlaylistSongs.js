import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../../axiosConfig';
import SongCard from '../CardComponents/SongCard';
import './PlaylistSongs.css';

const PlaylistSongs = () => {
  const { id } = useParams();
  const [songs, setSongs] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSongs = async () => {
      try {
        const response = await api.get(`/playlist/${id}/songs/`);
        setSongs(response.data);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching songs:', error);
        setError('Error fetching songs. Please try again later.');
        setIsLoading(false);
      }
    };

    fetchSongs();
  }, [id]);

  const handleSongClick = (clickedSong) => {
    localStorage.setItem('songQueue', JSON.stringify(songs));
    localStorage.setItem('currentSongId', clickedSong.id);
    window.dispatchEvent(new Event('storage'));
  };

  if (isLoading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <div className="playlist-page-songs">
      <div className="playlist-songs-header">
        <span>Song</span>
        <span>Created</span>
        <span><i className="fas fa-clock"></i></span>
        <span><i className="fas fa-headphones-alt"></i></span>
      </div>
      {songs.map(song => (
        <SongCard key={song.id} song={song} onSongClick={handleSongClick} />
      ))}
    </div>
  );
};

export default PlaylistSongs;
