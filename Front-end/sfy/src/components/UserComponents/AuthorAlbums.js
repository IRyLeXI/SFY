import React, { useState, useEffect } from 'react';
import api from '../../axiosConfig';
import AlbumCard from '../CardComponents/AlbumCard';
import './AuthorAlbums.css';

const AuthorAlbums = ({ userId }) => {
  const [albums, setAlbums] = useState([]);
  const [showAll, setShowAll] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [newAlbumTitle, setNewAlbumTitle] = useState('');
  const loggedInUserId = localStorage.getItem('user_id');

  useEffect(() => {
    const fetchAuthorAlbums = async () => {
      try {
        const response = await api.get(`/author/${userId}/albums/`);
        setAlbums(response.data);
      } catch (error) {
        console.error('Error fetching author albums:', error);
      }
    };

    fetchAuthorAlbums();
  }, [userId]);

  const handleAddAlbum = async (event) => {
    event.preventDefault();
    try {
      const response = await api.post('/album/create/', {
        title: newAlbumTitle,
        owner: userId,
      });
      setAlbums([...albums, response.data]);
      setShowForm(false);
      setNewAlbumTitle('');
    } catch (error) {
      console.error('Error creating new album:', error);
    }
  };

  if (albums.length === 0) {
    return <div className="no-albums">No albums yet</div>
  }

  const displayedAlbums = showAll ? albums : albums.slice(0, 6);

  return (
    <div className="author-albums">
      <div className="header">
        <h3>Author Albums</h3>
        {loggedInUserId === userId.toString() && (
          <button onClick={() => setShowForm(!showForm)} className="add-album-button">Add</button>
        )}
      </div>
      {showForm && (
        <form onSubmit={handleAddAlbum} className="add-album-form">
          <input
            type="text"
            placeholder="Album Title"
            value={newAlbumTitle}
            onChange={(e) => setNewAlbumTitle(e.target.value)}
            required
          />
          <button type="submit">Create</button>
        </form>
      )}
      <div className="album-cards-container">
        {displayedAlbums.map((album) => (
          <AlbumCard key={album.id} album={album} />
        ))}
      </div>
      {albums.length > 6 && (
        <button onClick={() => setShowAll(!showAll)} className="view-all-button">
          {showAll ? 'Show Less' : 'View All'}
        </button>
      )}
    </div>
  );
};

export default AuthorAlbums;
