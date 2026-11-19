document.addEventListener('DOMContentLoaded', () => {
    const header = document.querySelector('header nav');
    if (!header || document.querySelector('.menu-trigger')) return;

    const trigger = document.createElement('button');
    trigger.className = 'menu-trigger';
    trigger.type = 'button';
    trigger.setAttribute('aria-label', 'Open JobHunt menu');
    trigger.setAttribute('aria-expanded', 'false');
    trigger.innerHTML = '<span aria-hidden="true">☰</span> Menu';
    header.prepend(trigger);

    const drawer = document.createElement('aside');
    drawer.className = 'site-menu';
    drawer.setAttribute('aria-hidden', 'true');
    drawer.innerHTML = `<div class="site-menu-backdrop"></div><div class="site-menu-panel"><div class="site-menu-head"><strong>JobHunt menu</strong><button class="menu-close" type="button" aria-label="Close menu">×</button></div><nav class="menu-links"><p>Explore</p><a href="index.html">Home</a><a href="menu.html#company-reviews">Company Reviews</a><a href="menu.html#find-salaries">Find Salaries</a><a href="employer-dashboard.html">Employers</a><p>Account</p><a href="profile.html">Profile</a><a href="dashboard.html">My Jobs</a><a href="menu.html#reviews">Reviews</a><a href="menu.html#demographics">Demographics</a><a href="menu.html#matching-data">Matching Data</a><a href="menu.html#credentials">Credentials</a><a href="settings.html">Settings</a><a href="menu.html#country-language">Language</a><p>Legal and support</p><a href="menu.html#privacy">Privacy Center and Ad Choices</a><a href="menu.html#terms">Terms</a><a href="menu.html#accessibility">Accessibility at JobHunt</a><a href="menu.html#privacy-choices">Your Privacy Choices</a><a href="menu.html#help">Help</a><button class="menu-signout" type="button">Sign out <small>subashanil123@gmail.com</small></button></nav></div>`;
    document.body.appendChild(drawer);

    const helpSection = document.getElementById('help');
    if (helpSection && !helpSection.querySelector('.support-contact')) {
        const support = document.createElement('div');
        support.className = 'support-contact';
        support.innerHTML = '<strong>JobHunt Customer Care</strong><a href="mailto:huntsjob9@gmail.com?subject=Job Application">Email: huntsjob9@gmail.com</a><a href="tel:+9779741706478">Call: +977-9741706478</a><a href="mailto:huntsjob9@gmail.com?subject=JobHunt%20problem%20report">Report a problem by email</a>';
        helpSection.appendChild(support);
    }

    if (!document.querySelector('script[src*="i18n.js"]')) {
        const languageScript = document.createElement('script');
        languageScript.src = 'js/i18n.js';
        document.body.appendChild(languageScript);
    }

    function setOpen(isOpen) {
        drawer.classList.toggle('is-open', isOpen);
        drawer.setAttribute('aria-hidden', String(!isOpen));
        trigger.setAttribute('aria-expanded', String(isOpen));
        document.body.classList.toggle('menu-is-open', isOpen);
    }

    trigger.addEventListener('click', () => setOpen(true));
    drawer.querySelector('.menu-close').addEventListener('click', () => setOpen(false));
    drawer.querySelector('.site-menu-backdrop').addEventListener('click', () => setOpen(false));
    drawer.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setOpen(false)));
    drawer.querySelector('.menu-signout').addEventListener('click', async () => {
        await fetch('/api/logout/', { method: 'POST', credentials: 'same-origin' });
        window.location.href = 'index.html';
    });
    document.addEventListener('keydown', event => { if (event.key === 'Escape') setOpen(false); });
});
