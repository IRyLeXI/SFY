import React, { useState, useEffect } from 'react';
import api from '../../axiosConfig';
import SongCard from '../CardComponents/SongCard';
import CreateSongModal from '../UserComponents/CreateSongModal';
import './AuthorSongs.css';

const AuthorSongs = ({ userId }) => {
  const [songs, setSongs] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showAll, setShowAll] = useState(false);
  const [showForm, setShowForm] = useState(false);

  const loggedInUserId = localStorage.getItem('user_id');

  useEffect(() => {
    const fetchSongs = async () => {
      try {
        const response = await api.get(`/author/${userId}/songs/`);
        const sortedSongs = response.data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
        setSongs(sortedSongs);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching songs:', error);
        if (error.response && error.response.status === 404) {
          setError('This author has no songs yet.');
        } else {
          setError('Error fetching songs. Please try again later.');
        }
        setIsLoading(false);
      }
    };

    fetchSongs();
  }, [userId]);

  const handleSongClick = (clickedSong) => {
    localStorage.setItem('songQueue', JSON.stringify(songs));
    localStorage.setItem('currentSongId', clickedSong.id);
    window.dispatchEvent(new Event('storage'));
  };

  const handleSongCreated = async () => {
    const response = await api.get(`/author/${userId}/songs/`);
    const sortedSongs = response.data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    setSongs(sortedSongs);
  };

  if (isLoading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  const displayedSongs = showAll ? songs : songs.slice(0, 3);

  return (
    <div className="author-songs">
      <h3>Author Songs</h3>
      <div className="song-cards-container-author">
        {songs.length === 0 ? (
          <p>This author has no songs yet.</p>
        ) : (
          displayedSongs.map((song) => (
            <SongCard key={song.id} song={song} onSongClick={handleSongClick} />
          ))
        )}
      </div>
      {songs.length > 3 && (
        <button onClick={() => setShowAll(!showAll)} className="add-song-button-author">
          {showAll ? 'Show Less' : 'View All'}
        </button>
      )}
      {loggedInUserId === userId && (
        <button onClick={() => setShowForm(true)} className="add-song-button-author">
          Add Song
        </button>
      )}
      {showForm && <CreateSongModal userId={userId} onClose={() => setShowForm(false)} onSongCreated={handleSongCreated} />}
    </div>
  );
};

export default AuthorSongs;
