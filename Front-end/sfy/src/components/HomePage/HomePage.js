import React from 'react';
import HomeLogo from '../HomePageComponents/HomeLogo';
import DailyRecommendations from '../HomePageComponents/DailyRecommendations';
import RecommendedAlbums from '../HomePageComponents/RecommendedAlbums';
import SubscribedMusic from '../HomePageComponents/SubscribedMusic';

const HomePage = () => {
  return (
    <div className="home-page">
      <HomeLogo />
      <DailyRecommendations />
      <RecommendedAlbums />
      <SubscribedMusic />
    </div>
  );
};

export default HomePage;
