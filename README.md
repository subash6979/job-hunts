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
3. Set the environment variables listed in `.env.example`. `DJANGO_SECRET_KEY` is required; generate a unique key with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`. Do not commit the generated value.
4. Apply migrations: `python manage.py migrate`.
5. Start the app: `python manage.py runserver`.
6. Open `http://127.0.0.1:8000/` in your browser.

The application reads configuration from the process environment; `.env.example` is a template and is not loaded automatically. Keep actual `.env` files out of version control.

## Secrets and configuration

- `DJANGO_SECRET_KEY` is required and must be kept server-side. Do not put it in browser JavaScript or expose it through a client-prefixed environment variable.
- `DJANGO_DEBUG` defaults to `False`; set it to `True` only for local development.
- `DJANGO_ALLOWED_HOSTS` is a comma-separated list of permitted host names.
- The app currently uses a local SQLite database. It has no database connection URL or configured Supabase, Stripe, OAuth, or third-party API credentials.
- Rotate any secret that has ever been committed immediately; deleting it from the current source does not remove it from Git history. A development Django signing key was previously committed, so replace it with a new random value and invalidate existing sessions.

## User data collection and flow

| Data | Collection point | Destination and use |
| --- | --- | --- |
| Username, email, password | Registration form and `/api/register/` | Stored in Django's user table in SQLite; Django hashes the password. Login sends email/password to `/api/login/` for authentication, then Django maintains a server-side session using a session cookie. |
| Email and notification preferences | `/api/settings/` and settings page | Email is part of the Django user record. The three notification choices are stored in the `UserSettings` table; this app does not currently send notification email. |
| Resume file and cover note | `/api/jobs/<id>/apply/` | The API saves an `Application` record associated with the signed-in user and job, including uploaded resume and cover note. The current job details page links to login rather than providing a submission form. |
| Job listing details | Job-post form and `/api/post-job/` | The current form is not wired to the API. When `/api/post-job/` is called, title, company, location, role details, salary and related fields are stored in the `Job` table and returned by public job-search/detail APIs. |
| Job search terms and filters | Job search forms and `/api/jobs/` query parameters | Used to filter job records; the application does not persist the search values. |
| Saved/hidden job IDs and language choice | Browser `localStorage` | Stored only in that browser; these values are not account profile fields or sent to the backend by the current UI. |
| Full name, phone number, and resume | Profile form | The form is presentational and is not currently connected to an API or saved by this application. |
| Desired location, account type, work type, and category | Onboarding form | The form only navigates to the jobs page; these values are not submitted or persisted. Company/salary search widgets and the language selector in the menu are also not connected to a backend. |

The app does not currently collect date of birth, home address, payment details, IP address, or device identifiers in its own application code, and it has no configured third-party data integrations. Hosting and web-server providers may independently process IP addresses or request/device metadata in their operational logs; review those providers' retention and privacy settings.

Application API responses do not include passwords, signing keys, or database credentials. Do not add request-body or credential logging. Production deployments must keep debug mode disabled and protect uploaded resumes and database files with appropriate access controls.

## Usage Guidelines

- Users can register for a new account or log in to access their dashboard.
- Employers can post job listings through the post-job page.
- Job seekers can browse job listings and apply for positions directly through the application.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.