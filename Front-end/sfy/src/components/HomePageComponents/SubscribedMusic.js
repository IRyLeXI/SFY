import React, { useState, useEffect } from 'react';
import api from '../../axiosConfig';
import PlaylistCard from '../CardComponents/PlaylistCard';
import AlbumCard from '../CardComponents/AlbumCard';
import './SubscribedMusic.css';

const SubscribedMusic = () => {
  const [subscribedMusic, setSubscribedMusic] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchSubscribedMusic = async () => {
      try {
        const response = await api.get('/user/get/followed/music/');
        const { subscribed_albums, subscribed_playlists } = response.data;
        const mergedMusic = [...subscribed_albums, ...subscribed_playlists];
        setSubscribedMusic(mergedMusic);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching subscribed music:', error);
        setIsLoading(false);
      }
    };

    fetchSubscribedMusic();
  }, []);

  const getRandomItems = (items, count) => {
    const shuffled = items.sort(() => 0.5 - Math.random());
    return shuffled.slice(0, count);
  };

  return (
    <div className="subscribed-music">
      <h2>From Your Library</h2>
      {isLoading ? (
        <p>Loading...</p>
      ) : subscribedMusic.length === 0 ? (
        <p>No subscribed music yet</p>
      ) : (
        <div className="subscribed-cards-container">
          {getRandomItems(subscribedMusic, 6).map(item => (
            <div key={item.id}>
              {item.is_private !== undefined ? (
                <PlaylistCard playlist={item} />
              ) : (
                <AlbumCard album={item} />
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SubscribedMusic;
