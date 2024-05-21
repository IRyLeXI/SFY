import React, { useState, useEffect } from 'react';
import api from '../../axiosConfig';
import './CreateSongModal.css';

const CreateSongModal = ({ userId, onClose, onSongCreated }) => {
  const [newSong, setNewSong] = useState({ name: '', audio: null, picture: null });
  const [genres, setGenres] = useState([]);
  const [selectedGenres, setSelectedGenres] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    const fetchGenres = async () => {
      try {
        const response = await api.get(`/genre/search/?query=${searchQuery}`);
        setGenres(response.data);
      } catch (error) {
        console.error('Error fetching genres:', error);
      }
    };

    fetchGenres();
  }, [searchQuery]);

  const handleInputChange = (e) => {
    const { name, files, value } = e.target;
    setNewSong((prev) => ({
      ...prev,
      [name]: files ? files[0] : value,
    }));
  };

  const handleGenreChange = (genreId, priority) => {
    setSelectedGenres((prev) => {
      const existingGenre = prev.find((g) => g.genre_id === genreId);
      if (existingGenre) {
        return prev.map((g) =>
          g.genre_id === genreId ? { ...g, priority } : g
        );
      }
      return [...prev, { genre_id: genreId, priority }];
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setUploading(true);
    const formData = new FormData();
    formData.append('name', newSong.name);
    formData.append('audio', newSong.audio);
    formData.append('picture', newSong.picture);
    formData.append('authors', userId);

    try {
      const songResponse = await api.post('/song/create/', formData);
      const songId = songResponse.data.id;

      await api.patch(`/song/genres/${songId}/`, { genres: selectedGenres });

      setNewSong({ name: '', audio: null, picture: null });
      setSelectedGenres([]);
      onSongCreated();
      onClose();
    } catch (error) {
      console.error('Error creating song:', error);
    }
    setUploading(false);
  };

  const isGenreSelected = (genreId) => {
    return selectedGenres.some(g => g.genre_id === genreId);
  };

  return (
    <div className="modal">
      <div className="modal-content">
        <span className="close" onClick={onClose}>
          &times;
        </span>
        <form className="song-form" onSubmit={handleSubmit}>
          <div>
            <label>Song Name</label>
            <input type="text" name="name" value={newSong.name} onChange={handleInputChange} required />
          </div>
          <div>
            <label>Audio File</label>
            <input type="file" name="audio" accept="audio/*" onChange={handleInputChange} required />
          </div>
          <div>
            <label>Picture File</label>
            <input type="file" name="picture" accept="image/*" onChange={handleInputChange} required />
          </div>
          <div>
            <label>Genres</label>
            <input
              type="text"
              placeholder="Search for genres"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <div className="genre-list">
              {genres.map((genre) => (
                <div key={genre.id} className="genre-item">
                  <span>{genre.name}</span>
                  <select
                    onChange={(e) => handleGenreChange(genre.id, parseInt(e.target.value, 10))}
                    defaultValue={isGenreSelected(genre.id) ? selectedGenres.find(g => g.genre_id === genre.id).priority : ""}
                  >
                    <option value="" disabled>
                      Priority
                    </option>
                    {[1, 2, 3, 4, 5].map((p) => (
                      <option key={p} value={p}>
                        {p}
                      </option>
                    ))}
                  </select>
                </div>
              ))}
            </div>
          </div>
          <button type="submit" disabled={uploading} className='song-add-submit-buttom'>
            {uploading ? 'Uploading...' : 'Create Song'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default CreateSongModal;