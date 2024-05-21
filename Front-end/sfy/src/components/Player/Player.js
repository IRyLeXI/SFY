import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { getDownloadURL, ref } from 'firebase/storage';
import { storage } from '../../firebase';
import api from '../../axiosConfig';
import './Player.css';
import prev from '../../prev.png';
import next from '../../next.png';
import pause from '../../pause.png';

const Player = () => {
    const [song, setSong] = useState(null);
    const [isPlaying, setIsPlaying] = useState(false);
    const [currentTime, setCurrentTime] = useState(0);
    const [audioUrl, setAudioUrl] = useState('');
    const [pictureUrl, setPictureUrl] = useState('');
    const [volume, setVolume] = useState(1);
    const [songId, setSongId] = useState(localStorage.getItem('currentSongId'));
    const audioRef = useRef(null);

    const apiUrl = '/user/song_listen/';

    useEffect(() => {
        const handleStorageChange = async () => {
            const newSongId = localStorage.getItem('currentSongId');
            if (newSongId && newSongId !== songId) {
                await stopListening();
                setSongId(newSongId);
                setIsPlaying(true);
            }
        };

        window.addEventListener('storage', handleStorageChange);

        if (songId) {
            fetchSongData(songId);
        }

        return () => {
            window.removeEventListener('storage', handleStorageChange);
        };
    }, [songId]);

    const fetchSongData = useCallback(async (id) => {
        try {
            const response = await api.get(`/song/get/${id}/`);
            const songData = response.data;
            setSong(songData);

            const pictureRef = ref(storage, songData.picture_url);
            const audioRef = ref(storage, songData.audio_url);

            const pictureUrl = await getDownloadURL(pictureRef);
            const audioUrl = await getDownloadURL(audioRef);

            setPictureUrl(pictureUrl);
            setAudioUrl(audioUrl);
            setIsPlaying(true); // Automatically start playing the new song

            await startListening(id);
        } catch (error) {
            console.error('Error fetching song data:', error);
        }
    }, []);

    useEffect(() => {
        if (audioRef.current) {
            const playPromise = audioRef.current.play();
            if (playPromise !== undefined) {
                playPromise.catch(error => {
                    console.error('Error playing audio:', error);
                });
            }
        }
    }, [audioUrl]);

    useEffect(() => {
        if (audioRef.current) {
            audioRef.current.volume = volume;
        }
    }, [volume]);

    const startListening = useCallback(async (id, isSliderUsed = false, sliderStamp = null) => {
        try {
            await api.post(`${apiUrl}listen/`, {
                song_id: id,
                is_slider_used: isSliderUsed,
                slider_stamp: sliderStamp
            });
        } catch (error) {
            console.error('Error starting song listen:', error);
        }
    }, []);

    const stopListening = useCallback(async () => {
        try {
            await api.patch(`${apiUrl}stop/`, {
                duration: "00:00:01"
            });
        } catch (error) {
            console.error('Error stopping song listen:', error);
        }
    }, []);

    const handlePlayPause = () => {
        setIsPlaying(prevIsPlaying => {
            if (prevIsPlaying) {
                audioRef.current.pause(); // При натисканні на паузу зупиняємо програвання
            } else {
                audioRef.current.play(); // При натисканні на програвання починаємо програвання
            }
            return !prevIsPlaying; // Повертаємо змінений стан isPlaying
        });
    };

    const handleTimeUpdate = () => {
        if (audioRef.current) {
            setCurrentTime(audioRef.current.currentTime);
        }
    };

    const handleSliderChange = async (e) => {
        const newTime = e.target.value;
        if (audioRef.current) {
            audioRef.current.currentTime = newTime;
            setCurrentTime(newTime);
        }
    };

    const formatTime = (time) => {
        const minutes = Math.floor(time / 60);
        const seconds = Math.floor(time % 60).toString().padStart(2, '0');
        return `00:${minutes.toString().padStart(2, '0')}:${seconds}`;
    };

    const handleNextSong = () => {
        const songQueue = JSON.parse(localStorage.getItem('songQueue')) || [];
        const currentSongIndex = songQueue.findIndex(s => s.id.toString() === songId.toString());
        if (currentSongIndex >= 0 && currentSongIndex < songQueue.length - 1) {
            const nextSongId = songQueue[currentSongIndex + 1].id;
            localStorage.setItem('currentSongId', nextSongId);
            window.dispatchEvent(new Event('storage'));
        } else if (currentSongIndex === songQueue.length - 1) {
            const firstSongId = songQueue[0].id;
            localStorage.setItem('currentSongId', firstSongId);
            window.dispatchEvent(new Event('storage'));
        }
    };
    const handlePreviousSong = () => {
        const songQueue = JSON.parse(localStorage.getItem('songQueue')) || [];
        const currentSongIndex = songQueue.findIndex(s => s.id.toString() === songId.toString());
        if (currentSongIndex > 0) {
            const previousSongId = songQueue[currentSongIndex - 1].id;
            localStorage.setItem('currentSongId', previousSongId);
            window.dispatchEvent(new Event('storage'));
        }
    };

    useEffect(() => {
        if (audioRef.current) {
            audioRef.current.addEventListener('ended', handleNextSong);
            return () => {
                audioRef.current.removeEventListener('ended', handleNextSong);
            };
        }
    }, [audioRef.current, handleNextSong]);

    if (!song) {
        return null;
    }

    return (
        <div className={`player ${isPlaying ? 'playing' : ''}`}>
            <img src={pictureUrl} alt={song.name} className="player-picture" />
            <div className="player-info">
                <h3>{song.name}</h3>
                <Link to={`/user/${song.authors[0]}`}>Author {song.authors[0]}</Link>
            </div>
            <div className="player-controls">
                <input
                    type="range"
                    min="0"
                    max={audioRef.current ? audioRef.current.duration : 0}
                    value={currentTime}
                    onChange={handleSliderChange}
                    className="time-slider"
                />
                <div className="time-info">
                    <span>{formatTime(currentTime)}</span>
                    <span>{formatTime(audioRef.current ? audioRef.current.duration : 0)}</span>
                </div>
                <div className="control-buttons">
                    <button className="player-button" onClick={handlePreviousSong}>
                        <img src={prev} alt="Previous" />
                    </button>
                    <button onClick={handlePlayPause} className="player-button">
                        {isPlaying ? (
                            <img src={pause} alt="Pause" />
                        ) : (
                            <img src="https://cdn2.iconfinder.com/data/icons/basics-1/100/Play-512.png" alt="Play" />
                        )}
                    </button>
                    <button className="player-button" onClick={handleNextSong}>
                        <img src={next} alt="Next" />
                    </button>
                </div>
                <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.01"
                    value={volume}
                    onChange={(e) => setVolume(e.target.value)}
                    className="volume-slider"
                />
                <audio
                    ref={audioRef}
                    src={audioUrl}
                    onTimeUpdate={handleTimeUpdate}
                />
            </div>
        </div>
    );
}

export default Player;
