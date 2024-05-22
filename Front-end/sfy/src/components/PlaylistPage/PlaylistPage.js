import React from 'react';
import PlaylistInfo from '../PlaylistPageComponents/PlaylistInfo';
import PlaylistSongs from '../PlaylistPageComponents/PlaylistSongs';
import './PlaylistPage.css';


const PlaylistPage = () => {
  return (
    <div className="playlist-page">
      <PlaylistInfo />
      <PlaylistSongs />
    </div>
  );
};

export default PlaylistPage;
