import React, { useState, useEffect } from 'react';
import { getDownloadURL, ref } from 'firebase/storage';
import { storage } from '../../../firebase'; // Імпорт конфігурації Firebase
import './FollowedUserCard.css';

const FollowedUserCard = ({ user, onClick }) => {
    const [profilePictureUrl, setProfilePictureUrl] = useState('');

    useEffect(() => {
        const fetchProfilePicture = async () => {
            if (user.picture_url) {
                try {
                    const storageRef = ref(storage, user.picture_url);
                    const url = await getDownloadURL(storageRef);
                    setProfilePictureUrl(url);
                } catch (error) {
                    console.error('Error fetching profile picture:', error);
                }
            }
        };

        fetchProfilePicture();
    }, [user.picture_url]);

    return (
        <div className="followed-user-card" onClick={onClick}>
            <div className="card-image-container">
                <img
                    src={profilePictureUrl || 'default-profile-picture-url'}
                    alt={user.username}
                    className="user-card-picture"
                />
            </div>
            <div className="user-card-info">
                <h4>{user.username}</h4>
                <p>{user.is_author ? 'Author' : 'User'}</p>
            </div>
        </div>
    );
};

export default FollowedUserCard;
