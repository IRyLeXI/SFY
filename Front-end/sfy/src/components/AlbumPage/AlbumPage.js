import React from 'react';
import AlbumInfo from '../AlbumPageComponents/AlbumInfo';
import AlbumSongs from '../AlbumPageComponents/AlbumSongs';
import './AlbumPage.css';

const AlbumPage = () => {
  return (
    <div className="album-page">
      <AlbumInfo />
      <AlbumSongs />
    </div>
  );
};

export default AlbumPage;
