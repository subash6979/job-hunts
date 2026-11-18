document.addEventListener('DOMContentLoaded', async () => {
    const savedJobsContainer = document.getElementById('saved-jobs-list');
    if (savedJobsContainer) {
        const savedJobIds = JSON.parse(localStorage.getItem('savedJobIds') || '[]');
        if (savedJobIds.length) {
            const jobsResponse = await fetch('/api/jobs/');
            const savedJobs = (await jobsResponse.json()).filter(job => savedJobIds.includes(job.id));
            savedJobsContainer.innerHTML = savedJobs.map(job => `<div class="feature"><h3>${job.title}</h3><p>${job.company} · ${job.city || job.location}</p><a class="button" href="job-details.html?id=${job.id}">View job</a></div>`).join('');
        }
    }
    const applicationsContainer = document.getElementById('applications-list');
    if (!applicationsContainer) return;

    try {
        const response = await fetch('/api/applications/');
        if (response.status === 401) {
            applicationsContainer.innerHTML = '<div class="card"><h3>Log in to see your applications.</h3><a class="button" href="login.html">Log in</a></div>';
            return;
        }
        const applications = await response.json();
        if (!applications.length) {
            applicationsContainer.innerHTML = '<div class="card"><h3>Your application timeline starts here.</h3><p>Apply to a role and every update will appear in this view.</p><a class="button" href="jobs.html">Find a role</a></div>';
            return;
        }
        applicationsContainer.innerHTML = applications.map(application => `
            <div class="card"><h3>${application.jobTitle}</h3><p>${application.company}</p><span class="status">${application.status}</span><p>Updated ${new Date(application.updatedAt).toLocaleDateString()}</p></div>
        `).join('');
    } catch (error) {
        applicationsContainer.innerHTML = '<div class="card"><h3>We could not load your applications.</h3><p>Please refresh and try again.</p></div>';
    }
});