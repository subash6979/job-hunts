// auth.js

const API_URL = '/api';
const authMessage = document.getElementById('auth-message');

function showAuthMessage(message) {
    if (authMessage) authMessage.textContent = message;
}

// Function to handle user login
async function loginUser(email, password) {
    try {
        const response = await fetch(`${API_URL}/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'same-origin',
            body: JSON.stringify({ email, password }),
        });

        if (!response.ok) throw new Error((await response.json()).error || 'Login failed. Please check your credentials.');

        const data = await response.json();
        window.location.href = 'dashboard.html'; // Redirect to dashboard
    } catch (error) {
        showAuthMessage(error.message);
    }
}

// Function to handle user registration
async function registerUser(name, email, password) {
    try {
        const response = await fetch(`${API_URL}/register/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username: name, email, password }),
        });

        if (!response.ok) throw new Error((await response.json()).error || 'Registration failed. Please try again.');

        const data = await response.json();
        window.location.href = 'onboarding.html'; // Continue to profile setup
    } catch (error) {
        showAuthMessage(error.message);
    }
}

// Function to log out the user
function logoutUser() {
    sessionStorage.removeItem('token'); // Remove token from session storage
    window.location.href = 'index.html'; // Redirect to homepage
}

// Function to check if user is authenticated
function isAuthenticated() {
    return fetch(`${API_URL}/me/`, { credentials: 'same-origin' })
        .then(response => response.json())
        .then(data => data.authenticated);
}

const loginForm = document.getElementById('login-form');
if (loginForm) loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = e.target.email.value;
    const password = e.target.password.value;
    loginUser(email, password);
});

const registerForm = document.getElementById('register-form');
if (registerForm) registerForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = e.target.username.value;
    const email = e.target.email.value;
    const password = e.target.password.value;
    if (password !== e.target['confirm-password'].value) {
        showAuthMessage('Passwords do not match.');
        return;
    }
    registerUser(name, email, password);
});