// main.js

document.addEventListener("DOMContentLoaded", function() {
    // Initialize the application
    initApp();
});

function initApp() {
    // Set up event listeners or any initial setup needed for the application
    console.log("JobHunts application initialized.");
}

// Utility function to show alerts
function showAlert(message) {
    alert(message);
}

// Function to handle navigation
function navigateTo(page) {
    window.location.href = page;
}

// Function to fetch job data from jobs.json
async function fetchJobs() {
    try {
        const response = await fetch('data/jobs.json');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const jobs = await response.json();
        return jobs;
    } catch (error) {
        console.error('Error fetching jobs:', error);
    }
}

// Function to display jobs on jobs.html
function displayJobs(jobs) {
    const jobsContainer = document.getElementById('jobs-container');
    jobsContainer.innerHTML = ''; // Clear existing jobs

    jobs.forEach(job => {
        const jobElement = document.createElement('div');
        jobElement.classList.add('job-listing');
        jobElement.innerHTML = `
            <h3>${job.title}</h3>
            <p>${job.company}</p>
            <p>${job.location}</p>
            <a href="job-details.html?id=${job.id}">View Details</a>
        `;
        jobsContainer.appendChild(jobElement);
    });
}