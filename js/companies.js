document.addEventListener('DOMContentLoaded', async () => {
    const [response, extraResponse, sectorResponse] = await Promise.all([
        fetch('data/companies.json'),
        fetch('data/companies_extra.json'),
        fetch('data/companies_sectors.json')
    ]);
    const companies = [...await response.json(), ...await extraResponse.json(), ...await sectorResponse.json()];
    const list = document.getElementById('company-list');
    const filter = document.getElementById('company-country');
    const count = document.getElementById('company-count');
    const countries = [...new Set(companies.map(company => company.country))].sort();

    countries.forEach(country => filter.insertAdjacentHTML('beforeend', `<option value="${country}">${country}</option>`));

    function render() {
        const selected = filter.value;
        const visible = selected ? companies.filter(company => company.country === selected) : companies;
        count.textContent = `${visible.length} companies in the directory`;
        list.innerHTML = visible.map(company => `
            <article class="company-card">
                <div class="company-mark">${company.name.slice(0, 1)}</div>
                <div><h2>${company.name}</h2><p>${company.industry}</p><span class="tag">${company.city}, ${company.country}</span></div>
                <a class="apply-button" href="jobs.html?country=${encodeURIComponent(company.country)}">View jobs</a>
            </article>
        `).join('');
    }

    filter.addEventListener('change', render);
    render();
});
