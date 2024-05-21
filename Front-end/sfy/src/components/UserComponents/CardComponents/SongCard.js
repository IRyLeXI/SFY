import React, { useState, useEffect } from 'react';
import { getDownloadURL, ref } from 'firebase/storage';
import { storage } from '../../../firebase';
import './SongCard.css';

const SongCard = ({ song, onSongClick }) => {
  const [pictureUrl, setPictureUrl] = useState('');

  useEffect(() => {
    const fetchPictureUrl = async () => {
      try {
        const storageRef = ref(storage, song.picture_url);
        const url = await getDownloadURL(storageRef);
        setPictureUrl(url);
      } catch (error) {
        console.error('Error fetching song picture:', error);
      }
    };

    fetchPictureUrl();
  }, [song.picture_url]);

  const handleClick = () => {
    onSongClick(song);
  };

  return (
    <div className="song-card" onClick={handleClick}>
      <table>
        <tbody>
          <tr>
            <td><img src={pictureUrl} alt={song.name} className="song-picture" /></td>
            <td>
              <p>{song.name}</p>
              <p><a href={`/user/${song.authors[0]}`}>Author {song.authors[0]}</a></p>
            </td>
            <td><p>{new Date(song.publication_date).toLocaleDateString()}</p></td>
            <td><p>{song.duration}</p></td>
            <td><p>{song.listened_num}</p></td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default SongCard;
