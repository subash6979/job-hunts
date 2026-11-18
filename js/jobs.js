// JavaScript code for managing job listings in JoB HUnts application

let allJobs = [];
let locationCatalog = [];
let savedJobIds = JSON.parse(localStorage.getItem('savedJobIds') || '[]');
let hiddenJobIds = JSON.parse(localStorage.getItem('hiddenJobIds') || '[]');

async function fetchJobs() {
    try {
        const query = new URLSearchParams();
        const search = document.getElementById('search-input')?.value.trim();
        const country = document.getElementById('country-filter')?.value;
        const arrangement = document.getElementById('arrangement-filter')?.value;
        const selectedCategory = document.getElementById('category-filter')?.value;
        const category = new URLSearchParams(window.location.search).get('category');
        if (search) query.set('q', search);
        if (country) query.set('country', country);
        if (arrangement) query.set('work_arrangement', arrangement);
        if (selectedCategory || category) query.set('category', selectedCategory || category);
        const [response, locationsResponse] = await Promise.all([
            fetch(`/api/jobs/?${query}`),
            fetch('/data/countries.json')
        ]);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        allJobs = await response.json();
        locationCatalog = await locationsResponse.json();
        populateLocations(locationCatalog);
        displayJobs(allJobs);
    } catch (error) {
        console.error('Error fetching jobs:', error);
    }
}

// Function to display job listings on the jobs.html page
function populateLocations(countries) {
    const countryFilter = document.getElementById('country-filter');
    const locationFilter = document.getElementById('location-filter');
    const selectedCountry = countryFilter.value;
    countryFilter.innerHTML = '<option value="">Any country</option>' + countries.map(item => `<option value="${item.country}">${item.country}</option>`).join('');
    countryFilter.value = selectedCountry;
    const locations = countries.filter(item => !selectedCountry || item.country === selectedCountry).flatMap(item => item.cities).sort();
    locationFilter.innerHTML = '<option value="">Any city</option>';
    locations.forEach(location => {
        locationFilter.insertAdjacentHTML('beforeend', `<option value="${location}">${location}</option>`);
    });
}

function displayJobs(jobs) {
    const jobsContainer = document.getElementById('job-listings');
    const count = document.getElementById('job-count');
    jobsContainer.innerHTML = '';
    jobs = jobs.filter(job => !hiddenJobIds.includes(job.id));
    count.textContent = `${jobs.length} ${jobs.length === 1 ? 'opportunity' : 'opportunities'} worth a closer look`;

    jobs.forEach(job => {
        const jobElement = document.createElement('div');
        jobElement.classList.add('job-listing');

        const isSaved = savedJobIds.includes(job.id);
        jobElement.innerHTML = `
            <div class="job-card-head"><div class="job-card-actions"><button class="icon-action save-job" data-job-id="${job.id}" type="button" aria-label="${isSaved ? 'Remove saved job' : 'Save job'}">${isSaved ? 'Saved' : 'Save'}</button><button class="icon-action hide-job" data-job-id="${job.id}" type="button" aria-label="Not interested">Hide</button></div></div>
            <h3>${job.title}</h3>
            <p><strong>${job.company}</strong> ${job.companyVerified ? '<span class="tag">Verified company</span>' : ''}</p>
            <p>${job.city ? `${job.city}, ${job.country}` : job.location}</p>
            <p>${job.description}</p>
            <div class="job-meta"><span class="tag">${job.workArrangement || 'On-site'}</span><span class="tag">${job.employmentType || 'Full-time'}</span><span class="tag">${job.salary || 'Salary discussed'}</span></div>
            <a href="job-details.html?id=${job.id}" class="apply-button">Apply now</a>
        `;

        jobsContainer.appendChild(jobElement);
    });
    document.getElementById('saved-view').textContent = `Saved jobs (${savedJobIds.length})`;
}

function persistJobLists() {
    localStorage.setItem('savedJobIds', JSON.stringify(savedJobIds));
    localStorage.setItem('hiddenJobIds', JSON.stringify(hiddenJobIds));
}

document.addEventListener('DOMContentLoaded', () => {
    fetchJobs();
    document.getElementById('search-button')?.addEventListener('click', fetchJobs);
    document.getElementById('search-input')?.addEventListener('keydown', event => {
        if (event.key === 'Enter') fetchJobs();
    });
    document.getElementById('location-filter')?.addEventListener('change', () => {
        const selected = document.getElementById('location-filter').value;
        displayJobs(selected ? allJobs.filter(job => (job.city || job.location).toLowerCase().includes(selected.toLowerCase())) : allJobs);
    });
    document.getElementById('country-filter')?.addEventListener('change', () => {
        populateLocations(locationCatalog);
        fetchJobs();
    });
    document.getElementById('category-filter')?.addEventListener('change', fetchJobs);
    document.querySelectorAll('.quick-filter').forEach(button => button.addEventListener('click', () => {
        const type = button.dataset.type;
        displayJobs(type === 'entry-level' ? allJobs.filter(job => (job.title + job.description).toLowerCase().includes('entry')) : allJobs.filter(job => job.employmentType === type));
    }));
    document.getElementById('saved-view')?.addEventListener('click', () => displayJobs(allJobs.filter(job => savedJobIds.includes(job.id))));
    document.getElementById('job-listings')?.addEventListener('click', event => {
        const button = event.target.closest('button[data-job-id]');
        if (!button) return;
        const jobId = Number(button.dataset.jobId);
        if (button.classList.contains('save-job')) {
            savedJobIds = savedJobIds.includes(jobId) ? savedJobIds.filter(id => id !== jobId) : [...savedJobIds, jobId];
        } else {
            hiddenJobIds = [...new Set([...hiddenJobIds, jobId])];
        }
        persistJobLists();
        displayJobs(allJobs);
    });
});