import React, { useState } from 'react';
import api from '../../axiosConfig';
import './AuthorEditForm.css';

const AuthorEditForm = ({ user, onClose }) => {
    const [loading, setLoading] = useState(false);

    const handleEditInfo = async (event) => {
        event.preventDefault();
        setLoading(true);

        const formData = new FormData(event.target);

        try {
            await api.patch(`/user/patch/${user.id}/`, formData);
            onClose();
        } catch (error) {
            console.error('Error updating user info:', error);
        }
        setLoading(false);
    };

    return (
        <form onSubmit={handleEditInfo} className="edit-info-form-author">
            <label>
                Username:
                <input type="text" name="username" defaultValue={user.username} />
            </label>
            <label>
                Email:
                <input type="email" name="email" defaultValue={user.email} />
            </label>
            <label>
                Password:
                <input type="password" name="password" />
            </label>
            <label>
                First Name:
                <input type="text" name="first_name" defaultValue={user.first_name} />
            </label>
            <label>
                Last Name:
                <input type="text" name="last_name" defaultValue={user.last_name} />
            </label>
            <label>
                Birth Date:
                <input type="date" name="birth_date" defaultValue={user.birth_date} />
            </label>
            <button type="submit" disabled={loading}>Save</button>
            <button type="button" onClick={onClose}>Cancel</button>
        </form>
    );
};

export default AuthorEditForm;
