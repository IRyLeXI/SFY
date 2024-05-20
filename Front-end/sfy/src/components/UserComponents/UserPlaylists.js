import React, { useState, useEffect } from 'react';
import api from '../../axiosConfig';
import PlaylistCard from './CardComponents/PlaylistCard';
import './UserPlaylists.css';

const UserPlaylists = ({ userId }) => {
  const [playlists, setPlaylists] = useState([]);
  const [showAll, setShowAll] = useState(false);

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
  if (playlists === undefined || playlists.length===0) {
    return <div className="no-playlists">No playlists yet</div>
  }

  const displayedPlaylists = showAll ? playlists : playlists.slice(0, 6);

  return (
    <div className="user-playlists">
      <h3>User Playlists</h3>
      <div className="playlist-cards-container">
        {displayedPlaylists.map((playlist) => (
          <PlaylistCard key={playlist.id} playlist={playlist} />
        ))}
      </div>
      {playlists.length > 6 && (
        <button onClick={() => setShowAll(!showAll)} className="view-all-button">
          {showAll ? 'Show Less' : 'View All'}
        </button>
      )}
    </div>
  );
};

export default UserPlaylists;
