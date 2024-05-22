import React from 'react';
import SongCard from '../CardComponents/SongCard';
import FollowedUserCard from '../CardComponents/FollowedUserCard';
import AlbumCard from '../CardComponents/AlbumCard';
import './SearchResults.css';
import { useNavigate } from 'react-router-dom';

const SearchResults = ({ results, onSongClick }) => {
    const navigate = useNavigate();

    const handleUserClick = (id) => {
        navigate(`/user/${id}`);
    };

    return (
        <div className="search-results">
            {results.songs && results.songs.length > 0 && (
                <div className="results-section">
                    <h3>Songs</h3>
                    <div className="song-cards-container-search">
                        {results.songs.slice(0, 3).map((song) => (
                            <SongCard key={song.id} song={song} onSongClick={onSongClick} />
                        ))}
                    </div>
                </div>
            )}
            {results.authors && results.authors.length > 0 && (
                <div className="author-cards-container-search">
                    <h3>Authors</h3>
                    <div className="search-authors-container">
                        {results.authors.slice(0, 7).map((author) => (
                            <FollowedUserCard key={author.id} user={author} onClick={() => handleUserClick(author.id)} />
                        ))}
                    </div>
                </div>
            )}
            {results.albums && results.albums.length > 0 && (
                <div className="album-cards-container-search">
                    <h3>Albums</h3>
                    <div className="search-albums-container">
                        {results.albums.slice(0, 5).map((album) => (
                            <AlbumCard key={album.id} album={album} />
                        ))}
                    </div>
                </div>
            )}
            {results.users && results.users.length > 0 && (
                <div className="author-cards-container-search">
                    <h3>Users</h3>
                    <div className="search-authors-container">
                        {results.users.slice(0, 7).map((user) => (
                            <FollowedUserCard key={user.id} user={user} onClick={() => handleUserClick(user.id)} />
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default SearchResults;
