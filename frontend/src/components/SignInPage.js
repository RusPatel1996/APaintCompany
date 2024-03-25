import React, { useState } from 'react';
import axios from 'axios';
import  { useNavigate } from 'react-router-dom'
import { API_URL } from '.';

function SignInPage() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    let navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post(API_URL + 'login/', {
                username,
                password,
            }); 
            console.log(response.data.message);
            navigate('/inventory');
        } catch (error) {
            setError(error.response.data.error);
        }
    };

    return (
        <div>
            <h2>Sign In</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>} 
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Username:</label>
                    <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
                </div>
                <div>
                    <label>Password:</label>
                    <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                </div>
                <button type="submit">Sign In</button>
            </form>
        </div>
    );
}

export default SignInPage;