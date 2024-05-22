import React, { useState, useEffect } from 'react';
import { getDownloadURL, ref } from 'firebase/storage';
import { storage } from '../../firebase';
import { useNavigate } from 'react-router-dom';
import api from '../../axiosConfig';
import './SongCard.css';

const SongCard = ({ song, onSongClick }) => {
  const [pictureUrl, setPictureUrl] = useState('');
  const [showMenu, setShowMenu] = useState(false);
  const [playlists, setPlaylists] = useState([]);
  const [showPlaylists, setShowPlaylists] = useState(false);
  const [loadingPlaylists, setLoadingPlaylists] = useState(false);
  const [error, setError] = useState('');
  const loggedInUserId = localStorage.getItem('user_id');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPictureUrl = async () => {
      try {
        const storageRef = ref(storage, song.picture_url);
        const url = await getDownloadURL(storageRef);
        setPictureUrl(url);
      } catch (error) {
        console.error('Error fetching song picture:', error);
      }
    };

    fetchPictureUrl();
  }, [song.picture_url]);

  const toggleMenu = (event) => {
    event.stopPropagation();
    setShowMenu(!showMenu);
  };

  const handleAddToPlaylistClick = async (event) => {
    event.stopPropagation();
    if (!loggedInUserId) {
      setError('You need to log in to add songs to playlists.');
      return;
    }

    setLoadingPlaylists(true);
    try {
      const response = await api.get(`/user/get/${loggedInUserId}/playlists/`);
      setPlaylists(response.data);
      setShowPlaylists(true);
      if (response.data.length === 0) {
        setError('No playlists found');
      }
    } catch (error) {
      console.error('Error fetching playlists:', error);
      setError('Error fetching playlists');
    }
    setLoadingPlaylists(false);
  };

  const handleAddSongToPlaylist = async (playlistId) => {
    try {
      await api.post(`/playlist/${playlistId}/add_song/`, { song_id: song.id });
      setShowPlaylists(false);
      setShowMenu(false);
      alert('Song added to playlist');
    } catch (error) {
      console.error('Error adding song to playlist:', error);
      alert('Error adding song to playlist');
    }
  };

  const handleSongRadioClick = async (event) => {
    event.stopPropagation();
    if (!loggedInUserId) {
      setError('You need to log in to access song radio.');
      return;
    }

    try {
      const response = await api.post('/playlist/radio/', { song_id: song.id });
      navigate(`/playlist/${response.data.id}`);
    } catch (error) {
      console.error('Error creating song radio playlist:', error);
      alert('Error creating song radio playlist');
    }
  };

  return (
    <div className="song-card">
      <table>
        <tbody>
          <tr>
            <td onClick={() => onSongClick(song)}>
              <img src={pictureUrl} alt={song.name} className="song-picture" />
            </td>
            <td onClick={() => onSongClick(song)}>
              <p>{song.name}</p>
              <p><a href={`/user/${song.authors[0]}`}>{song.authors_names}</a></p>
            </td>
            <td><p>{new Date(song.publication_date).toLocaleDateString()}</p></td>
            <td><p>{song.duration}</p></td>
            <td><p>{song.listened_num}</p></td>
            <td>
              <button onClick={toggleMenu} className="menu-button">
                &#x22EE;
              </button>
              {showMenu && (
                <div className="menu">
                  <button onClick={handleAddToPlaylistClick}>Add to playlist</button>
                  {loggedInUserId && (
                    <button onClick={handleSongRadioClick}>Song Radio</button>
                  )}
                </div>
              )}
              {showPlaylists && (
                <div className="playlist-menu">
                  {loadingPlaylists ? (
                    <p>Loading playlists...</p>
                  ) : error ? (
                    <p>{error}</p>
                  ) : (
                    playlists.map((playlist) => (
                      <button
                        key={playlist.id}
                        onClick={(e) => {
                          e.stopPropagation();
                          handleAddSongToPlaylist(playlist.id);
                        }}
                      >
                        {playlist.title}
                      </button>
                    ))
                  )}
                </div>
              )}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default SongCard;
