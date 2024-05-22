import React, { useState, useEffect } from 'react';
import api from '../../axiosConfig';
import PlaylistCard from '../CardComponents/PlaylistCard';
import './UserPlaylists.css';

const UserPlaylists = ({ userId }) => {
  const [playlists, setPlaylists] = useState([]);
  const [showAll, setShowAll] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [newPlaylistTitle, setNewPlaylistTitle] = useState('');
  const [isPrivate, setIsPrivate] = useState(false);
  const loggedInUserId = localStorage.getItem('user_id');

  useEffect(() => {
    const fetchUserPlaylists = async () => {
      try {
        const response = await api.get(`/user/get/${userId}/playlists/`);
        setPlaylists(response.data);
      } catch (error) {
        console.error('Error fetching user playlists:', error);
      }
    };

    fetchUserPlaylists();
  }, [userId]);

  const handleAddPlaylist = async (event) => {
    event.preventDefault();
    try {
      const response = await api.post('/playlist/create/', {
        title: newPlaylistTitle,
        is_private: isPrivate,
        is_generated: false,
        owner: userId,
      });
      setPlaylists([...playlists, response.data]);
      setShowForm(false);
      setNewPlaylistTitle('');
      setIsPrivate(false);
    } catch (error) {
      console.error('Error creating new playlist:', error);
    }
  };

  if (playlists === undefined || playlists.length === 0) {
    return <div className="no-playlists">No playlists yet</div>;
  }

  const displayedPlaylists = showAll ? playlists : playlists.slice(0, 6);

  return (
    <div className="user-playlists">
      <div className="header">
        <h3>User Playlists</h3>
        {loggedInUserId === userId.toString() && (
          <button onClick={() => setShowForm(!showForm)} className="add-playlist-button">Add</button>
        )}
      </div>
      {showForm && (
        <form onSubmit={handleAddPlaylist} className="add-playlist-form">
          <input
            type="text"
            placeholder="Playlist Title"
            value={newPlaylistTitle}
            onChange={(e) => setNewPlaylistTitle(e.target.value)}
            required
          />
          <label>
            Private
            <input
              type="checkbox"
              checked={isPrivate}
              onChange={(e) => setIsPrivate(e.target.checked)}
            />
          </label>
          <button type="submit">Create</button>
        </form>
      )}
      <div className="playlist-cards-container">
        {displayedPlaylists.map((playlist) => (
          <PlaylistCard key={playlist.id} playlist={playlist} />
        ))}
      </div>
      {playlists.length > 6 && (
        <button onClick={() => setShowAll(!showAll)} className="view-all-button-playlists">
          {showAll ? 'Show Less' : 'View All'}
        </button>
      )}
    </div>
  );
};

export default UserPlaylists;
