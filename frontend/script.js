import axios from 'axios';
document.getElementById('registration-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    try {
        const response = await axios.post('http://localhost:5000/api/auth/register', data);
        document.getElementById('registration-status').textContent = response.data.message;
    } catch (error) {
        document.getElementById('registration-status').textContent = 'Registration failed';
    }
});