document.addEventListener('DOMContentLoaded', async () => {
    await fetch('/api/logout/', { method: 'POST', credentials: 'same-origin' });
    window.location.href = 'index.html';
});
