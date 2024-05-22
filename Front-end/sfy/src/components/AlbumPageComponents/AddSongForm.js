import React, { useState, useEffect } from 'react';
import api from '../../axiosConfig';
import './AddSongForm.css';

const AddSongForm = ({ albumId, onClose }) => {
  const [songs, setSongs] = useState([]);
  const [selectedSong, setSelectedSong] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSongs = async () => {
      try {
        const response = await api.get(`/author/created_songs/`);
        setSongs(response.data);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching songs:', error);
        setError('Error fetching songs. Please try again later.');
        setIsLoading(false);
      }
    };

    fetchSongs();
  }, []);

  const handleAddSong = async () => {
    try {
      await api.post(`/album/${albumId}/add_song/`, { song_id: selectedSong });
      onClose();
    } catch (error) {
      console.error('Error adding song to album:', error);
    }
  };

  if (isLoading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <div className="add-song-form">
      <h2>Add Song to Album</h2>
      <select value={selectedSong} onChange={(e) => setSelectedSong(e.target.value)}>
        <option value="" disabled>Select a song</option>
        {songs.map((song) => (
          <option key={song.id} value={song.id}>
            {song.name}
          </option>
        ))}
      </select>
      <button onClick={handleAddSong}>Add Song</button>
      <button onClick={onClose}>Cancel</button>
    </div>
  );
};

export default AddSongForm;
