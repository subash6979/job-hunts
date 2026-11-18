document.addEventListener('DOMContentLoaded', async () => {
    const message = document.getElementById('settings-message');
    const showMessage = text => { message.textContent = text; };
    const settingsResponse = await fetch('/api/settings/', { credentials: 'same-origin' });
    if (settingsResponse.status === 401) {
        showMessage('Please log in to manage account settings.');
        return;
    }
    const settings = await settingsResponse.json();
    document.getElementById('email-job-alerts').checked = settings.emailJobAlerts;
    document.getElementById('email-application-updates').checked = settings.emailApplicationUpdates;
    document.getElementById('email-product-updates').checked = settings.emailProductUpdates;

    document.getElementById('save-notifications').addEventListener('click', async () => {
        await fetch('/api/settings/', {
            method: 'PATCH', credentials: 'same-origin', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email_job_alerts: document.getElementById('email-job-alerts').checked,
                email_application_updates: document.getElementById('email-application-updates').checked,
                email_product_updates: document.getElementById('email-product-updates').checked
            })
        });
        showMessage('Notification preferences saved.');
    });

    document.getElementById('password-form').addEventListener('submit', async event => {
        event.preventDefault();
        const newPassword = document.getElementById('new-password').value;
        if (newPassword !== document.getElementById('confirm-password').value) {
            showMessage('New passwords do not match.');
            return;
        }
        const response = await fetch('/api/password/', {
            method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ currentPassword: document.getElementById('current-password').value, newPassword })
        });
        const result = await response.json();
        showMessage(result.message || result.error);
        if (response.ok) event.target.reset();
    });

    document.getElementById('delete-account').addEventListener('click', async () => {
        if (prompt('Type DELETE to permanently remove your account.') !== 'DELETE') return;
        const response = await fetch('/api/delete-account/', {
            method: 'DELETE', credentials: 'same-origin', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ confirmation: 'DELETE' })
        });
        if (response.ok) window.location.href = 'index.html';
        else showMessage((await response.json()).error);
    });
});
