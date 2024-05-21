import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar/Navbar';
import LoginPage from './components/Auth/LoginPage';
import UserPage from './components/UserPage/UserPage';
import HomePage from './components/HomePage/HomePage';
import PlaylistPage from './components/PlaylistPage/PlaylistPage';
import Player from './components/Player/Player';
// import SearchPage from './components/SearchPage/SearchPage';
import './App.css';

function App() {
  const [isNavbarOpen, setIsNavbarOpen] = useState(false);

  return (
    <Router>
      <Player />
      <Navbar isOpen={isNavbarOpen} setIsOpen={setIsNavbarOpen} />
      <div className={`main-content ${isNavbarOpen ? 'shifted' : ''}`}>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/user/:id" element={<UserPage />} />
          <Route path="/" element={<HomePage />} />
          <Route path="/playlist/:id" element={<PlaylistPage />} />
          {/* <Route path="/search" element={<SearchPage />} /> */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;