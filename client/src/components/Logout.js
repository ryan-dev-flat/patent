import axios from 'axios';

const logout = async () => {
    try {
        await axios.post('http://127.0.0.1:5000/api/logout', {}, {
            withCredentials: true
        });
        // Clear user data from local storage or state
        localStorage.removeItem('token');
        // Redirect to login or home page
        window.location.href = '/login';
    } catch (error) {
        console.error('Logout failed', error);
    }
};

const Logout = () => {
    return (
        <button onClick={logout}>Logout</button>
    );
};

export default Logout;
