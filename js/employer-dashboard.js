const employerSearchInput = document.getElementById('employer-job-search');
const employerCountryFilter = document.getElementById('employer-country-filter');
const employerSearchButton = document.getElementById('employer-search-button');
const employerJobCount = document.getElementById('employer-job-count');
const employerJobListings = document.getElementById('employer-job-listings');

function renderEmployerJobs(jobs) {
    employerJobCount.textContent = `${jobs.length} ${jobs.length === 1 ? 'job' : 'jobs'} found`;
    employerJobListings.innerHTML = jobs.map(job => `
        <article class="card">
            <h3>${job.title}</h3>
            <p><strong>${job.company}</strong>${job.companyVerified ? ' · Verified company' : ''}</p>
            <p>${job.city ? `${job.city}, ${job.country}` : job.location}</p>
            <div class="job-meta">
                <span class="tag">${job.employmentType || 'Full-time'}</span>
                <span class="tag">${job.experienceLevel || 'Mid level'}</span>
                <span class="tag">${job.workArrangement || 'On-site'}</span>
                <span class="tag">${job.salary || 'Salary discussed'}</span>
            </div>
            <h4>Requirements</h4>
            <ul>${(job.requirements || []).map(requirement => `<li>${requirement}</li>`).join('')}</ul>
            <h4>Benefits</h4>
            <ul>${(job.benefits || []).map(benefit => `<li>${benefit}</li>`).join('')}</ul>
            <a class="button" href="job-details.html?id=${job.id}">View job</a>
        </article>
    `).join('');
}

async function loadEmployerCountries() {
    const response = await fetch('/data/countries.json');
    const countries = await response.json();
    employerCountryFilter.innerHTML = '<option value="">Any country</option>' + countries
        .map(item => `<option value="${item.country}">${item.country}</option>`)
        .join('');
}

async function searchEmployerJobs() {
    const query = new URLSearchParams();
    const search = employerSearchInput.value.trim();
    const country = employerCountryFilter.value;
    if (search) query.set('q', search);
    if (country) query.set('country', country);

    employerJobCount.textContent = 'Searching...';
    const response = await fetch(`/api/jobs/?${query}`);
    if (!response.ok) {
        employerJobCount.textContent = 'Jobs could not be loaded.';
        employerJobListings.innerHTML = '';
        return;
    }
    renderEmployerJobs(await response.json());
}

loadEmployerCountries().then(searchEmployerJobs).catch(() => {
    employerJobCount.textContent = 'Countries could not be loaded.';
});
employerSearchButton.addEventListener('click', searchEmployerJobs);
employerCountryFilter.addEventListener('change', searchEmployerJobs);
employerSearchInput.addEventListener('keydown', event => {
    if (event.key === 'Enter') searchEmployerJobs();
});
