import React, { useState } from 'react';
import api from '../../axiosConfig';
import PopularGenres from '../SearchPageComponents/PopularGenres';
import SearchResults from '../SearchPageComponents/SearchResults';
import './SearchPage.css';

const SearchPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState(null);

  const handleSearchChange = async (event) => {
    const query = event.target.value;
    setSearchQuery(query);

    if (query) {
      try {
        const response = await api.get('/user/search/', {
          params: { query }
        });
        setSearchResults(response.data);
      } catch (error) {
        console.error('Error fetching search results:', error);
        setSearchResults(null);
      }
    } else {
      setSearchResults(null);
    }
  };

  const handleSongClick = (clickedSong) => {
    if (searchResults && searchResults.songs) {
      localStorage.setItem('songQueue', JSON.stringify(searchResults.songs));
      localStorage.setItem('currentSongId', clickedSong.id);
      window.dispatchEvent(new Event('storage'));
    }
  };

  return (
    <div className="search-page">
      <input
        type="text"
        placeholder="Search..."
        value={searchQuery}
        onChange={handleSearchChange}
        className="search-input"
      />
      {searchQuery && searchResults ? (
        <SearchResults results={searchResults} onSongClick={handleSongClick} />
      ) : (
        <PopularGenres />
      )}
    </div>
  );
};

export default SearchPage;
