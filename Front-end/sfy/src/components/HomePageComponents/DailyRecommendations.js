import React, { useState, useEffect } from 'react';
import api from '../../axiosConfig';
import PlaylistCard from '../UserComponents/CardComponents/PlaylistCard';
import './DailyRecommendations.css';

const DailyRecommendations = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        const response = await api.get('/playlist/get/recommendations/');
        setRecommendations(response.data);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching recommendations:', error);
        setIsLoading(false);
      }
    };

    fetchRecommendations();
  }, []);

  return (
    <div className="daily-recommendations">
      <h2>Daily Recommendations</h2>
      {isLoading ? (
        <p>Loading...</p>
      ) : recommendations.length === 0 ? (
        <p>Login to receive your daily recommendations!</p>
      ) : (
        <div className="recommendations-list">
          {recommendations.map(playlist => (
            <PlaylistCard key={playlist.id} playlist={playlist} />
          ))}
        </div>
      )}
    </div>
  );
};

export default DailyRecommendations;
