# JobHunts

JobHunts is an online job portal designed to connect job seekers with employers. This application provides a user-friendly interface for browsing job listings, applying for jobs, and managing user profiles.

## Features

- **Homepage**: The main entry point of the application with navigation links to other sections.
- **Job Listings**: A dedicated page to view and search for job postings fetched from a JSON file.
- **Company Profiles**: A section that lists companies currently hiring, along with links to their job postings.
- **User Authentication**: Login and registration forms for users to create accounts and access personalized features.
- **User Dashboard**: A personalized dashboard displaying saved jobs, applications, and user profile information.
- **Job Posting**: A feature for employers to post new job listings with detailed job descriptions.
- **User Profile Management**: Users can view and edit their profile information, including resumes and contact details.
- **Candidate workspace**: Track applications through submitted, reviewing, interview, offer, rejected, and hired stages.
- **Employer workspace**: Review a hiring pipeline, post roles, and surface company verification signals.
- **Trust-aware search**: Filter by role, location, work arrangement, employment type, and salary metadata.
- **Django API**: SQLite-backed jobs, accounts, resume uploads, applications, and session authentication.

## Project Structure

```
job-hunts
├── index.html          # Main entry point of the application
├── jobs.html           # Displays job postings
├── companies.html       # Lists companies hiring
├── login.html          # User login form
├── register.html       # User registration form
├── dashboard.html      # User dashboard
├── post-job.html       # Form for employers to post jobs
├── profile.html        # User profile page
├── css
│   ├── style.css       # Main styles
│   ├── responsive.css   # Responsive design styles
│   └── theme.css       # Theme-specific styles
├── js
│   ├── app.js          # Main JavaScript file
│   ├── auth.js         # Authentication functions
│   ├── jobs.js         # Job listing functions
│   ├── dashboard.js     # Dashboard functionality
│   └── main.js         # General utility functions
├── assets
│   ├── images
│   │   └── logo.svg    # Logo image
│   └── icons
│       └── favicon.svg  # Favicon for the application
├── data
│   └── jobs.json       # Sample job data in JSON format
└── README.md           # Project documentation
```

## Setup Instructions

1. Install Python 3.12+.
2. Install dependencies: `python -m pip install -r requirements.txt`.
3. Apply migrations: `python manage.py migrate`.
4. Start the app: `python manage.py runserver`.
5. Open `http://127.0.0.1:8000/` in your browser.

## Usage Guidelines

- Users can register for a new account or log in to access their dashboard.
- Employers can post job listings through the post-job page.
- Job seekers can browse job listings and apply for positions directly through the application.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.