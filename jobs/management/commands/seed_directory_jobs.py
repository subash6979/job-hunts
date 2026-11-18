import json
from pathlib import Path

from django.core.management.base import BaseCommand

from jobs.models import Job


TITLE_BY_INDUSTRY = {
    "Technology": "Software Engineer",
    "E-commerce": "E-commerce Specialist",
    "Financial Services": "Financial Analyst",
    "Banking": "Customer Support Associate",
    "Healthcare": "Healthcare Coordinator",
    "Automotive": "Operations Associate",
    "Electronics": "Technical Support Specialist",
    "Telecommunications": "Network Support Specialist",
    "Education": "Education Program Assistant",
    "Construction": "Project Coordinator",
    "Aerospace": "Operations Engineer",
    "Retail": "Retail Team Lead",
    "Consulting": "Business Analyst",
    "Food & Beverage": "Operations Coordinator",
    "Media": "Content Coordinator",
    "Engineering": "Project Engineer",
    "Insurance": "Insurance Analyst",
    "Skilled Trades": "Skilled Trades Technician",
    "Transportation": "Transport Coordinator",
    "Education": "Teaching Assistant",
    "Hospitality & Retail": "Guest Services Associate",
}

CURRENCY_BY_COUNTRY = {
    "Canada": "CAD",
    "United States": "USD",
    "Nepal": "NPR",
    "Japan": "JPY",
    "South Korea": "KRW",
    "Ireland": "EUR",
    "United Kingdom": "GBP",
    "Germany": "EUR",
    "India": "INR",
    "China": "CNY",
    "Hong Kong": "HKD",
}

ADDITIONAL_JOBS = [
    {
        "title": "Part-time Customer Support Assistant",
        "company": "Northstar Community Services",
        "city": "Toronto",
        "country": "Canada",
        "category": "Business Services",
        "work_arrangement": "hybrid",
        "employment_type": "part-time",
        "salary": "CAD 22 - 28 per hour",
        "salary_currency": "CAD",
        "experience_level": "entry-level",
        "description": "Support customers by email and phone for 20 to 25 hours per week. This part-time role includes paid training and flexible weekday shifts.",
        "requirements": "Clear written and verbal communication\nComfort with basic computer tools\nReliable weekday availability",
        "benefits": "Paid training\nPaid statutory holidays\nEmployee assistance program",
    },
    {
        "title": "Part-time Retail Associate",
        "company": "Greenway Market",
        "city": "London",
        "country": "United Kingdom",
        "category": "Hospitality & Retail",
        "work_arrangement": "on-site",
        "employment_type": "part-time",
        "salary": "GBP 13 - 15 per hour",
        "salary_currency": "GBP",
        "experience_level": "entry-level",
        "description": "Help customers, restock products, and keep the shop floor welcoming during flexible part-time shifts.",
        "requirements": "Friendly customer service\nAbility to work some evenings or weekends\nNo previous retail experience required",
        "benefits": "Staff discount\nPaid holiday allowance\nFlexible shift scheduling",
    },
    {
        "title": "Software Engineering Intern",
        "company": "Brightpath Labs",
        "city": "Bengaluru",
        "country": "India",
        "category": "IT & Technology",
        "work_arrangement": "hybrid",
        "employment_type": "internship",
        "salary": "INR 25,000 - 35,000 per month",
        "salary_currency": "INR",
        "experience_level": "entry-level",
        "description": "Learn from experienced engineers while building and testing web features in a supported internship program.",
        "requirements": "Coursework or projects in programming\nBasic JavaScript or Python\nInterest in software development",
        "benefits": "Mentor support\nLearning budget\nCompletion certificate\nPaid sick leave",
    },
    {
        "title": "Marketing Intern",
        "company": "Harbor & Pine",
        "city": "Dublin",
        "country": "Ireland",
        "category": "Media",
        "work_arrangement": "remote",
        "employment_type": "internship",
        "salary": "EUR 14 - 16 per hour",
        "salary_currency": "EUR",
        "experience_level": "entry-level",
        "description": "Assist with social media, newsletters, and campaign research while gaining practical marketing experience through a paid internship.",
        "requirements": "Strong writing skills\nInterest in digital media\nOrganized approach to deadlines",
        "benefits": "Mentorship\nHybrid flexibility\nPaid annual leave\nTeam events",
    },
    {
        "title": "Entry-level Healthcare Coordinator",
        "company": "CareBridge Health",
        "city": "Chicago",
        "country": "United States",
        "category": "Healthcare",
        "work_arrangement": "on-site",
        "employment_type": "full-time",
        "salary": "USD 42,000 - 50,000",
        "salary_currency": "USD",
        "experience_level": "entry-level",
        "description": "Entry-level opportunity supporting patient scheduling and office coordination. Full training is provided for someone beginning a healthcare career.",
        "requirements": "High school diploma or equivalent\nEmpathy and attention to detail\nComfort learning scheduling software",
        "benefits": "Health insurance\nPaid holidays\nPaid training\nRetirement plan",
    },
    {
        "title": "Entry-level Data Support Analyst",
        "company": "Summit Data Works",
        "city": "New York",
        "country": "United States",
        "category": "IT & Technology",
        "work_arrangement": "remote",
        "employment_type": "full-time",
        "salary": "USD 52,000 - 62,000",
        "salary_currency": "USD",
        "experience_level": "entry-level",
        "description": "Entry-level role helping the analytics team clean records, prepare reports, and answer internal data questions.",
        "requirements": "Basic spreadsheet skills\nCuriosity and careful problem solving\nRelevant coursework or personal projects welcome",
        "benefits": "Health, dental, and vision insurance\nPaid time off\nRemote-work stipend\nProfessional development budget",
    },
]


class Command(BaseCommand):
    help = "Seed directory jobs for every supported country and city."

    def handle(self, *args, **options):
        base_dir = Path(__file__).resolve().parents[3]
        countries = json.loads((base_dir / "data" / "countries.json").read_text(encoding="utf-8"))
        companies = json.loads((base_dir / "data" / "companies.json").read_text(encoding="utf-8"))
        companies.extend(json.loads((base_dir / "data" / "companies_extra.json").read_text(encoding="utf-8")))
        companies.extend(json.loads((base_dir / "data" / "companies_sectors.json").read_text(encoding="utf-8")))
        created = 0

        for country_data in countries:
            country = country_data["country"]
            currency = CURRENCY_BY_COUNTRY[country]
            country_companies = [item for item in companies if item["country"] == country]
            for city in country_data["cities"]:
                company = next((item for item in country_companies if item["city"] == city), None)
                company_name = company["name"] if company else f"{city} Local Hiring Partners"
                industry = company["industry"] if company else "Business Services"
                title = TITLE_BY_INDUSTRY.get(industry, "Operations Coordinator")
                _, was_created = Job.objects.get_or_create(
                    title=title,
                    company=company_name,
                    city=city,
                    country=country,
                    defaults={
                        "location": f"{city}, {country}",
                        "category": "IT & Technology" if industry == "Technology" else industry,
                        "work_arrangement": "hybrid",
                        "employment_type": "full-time",
                        "experience_level": "mid-level",
                        "salary": f"{currency} salary range available",
                        "salary_currency": currency,
                        "description": f"Opportunity for the {company_name} team in {city}. Check the employer profile and application details before applying.",
                        "requirements": "Relevant experience or transferable skills\nClear communication\nInterest in learning",
                        "benefits": "Paid time off\nPublic holiday allowance\nEmployee assistance program",
                        "company_verified": bool(company),
                    },
                )
                created += int(was_created)

        for company in companies:
            country = company["country"]
            currency = CURRENCY_BY_COUNTRY[country]
            industry = company["industry"]
            title = TITLE_BY_INDUSTRY.get(industry, "Operations Coordinator")
            _, was_created = Job.objects.get_or_create(
                title=title,
                company=company["name"],
                city=company["city"],
                country=country,
                defaults={
                    "location": f"{company['city']}, {country}",
                    "category": "IT & Technology" if industry == "Technology" else industry,
                    "work_arrangement": "hybrid",
                    "employment_type": "full-time",
                    "experience_level": "mid-level",
                    "salary": f"{currency} salary range available",
                    "salary_currency": currency,
                    "description": f"Opportunity with {company['name']} in {company['city']}. Check the employer profile and application details before applying.",
                    "requirements": "Relevant experience or transferable skills\nClear communication\nInterest in learning",
                    "benefits": "Paid time off\nPublic holiday allowance\nEmployee assistance program",
                    "company_verified": False,
                },
            )
            created += int(was_created)

        for item in ADDITIONAL_JOBS:
            job, was_created = Job.objects.get_or_create(
                title=item["title"],
                company=item["company"],
                city=item["city"],
                country=item["country"],
                defaults={
                    **item,
                    "location": f'{item["city"]}, {item["country"]}',
                    "company_verified": True,
                },
            )
            job.experience_level = item["experience_level"]
            job.benefits = item["benefits"]
            job.save(update_fields=["experience_level", "benefits"])
            created += int(was_created)

        updated = Job.objects.filter(benefits="").update(
            benefits="Paid time off\nPublic holiday allowance\nEmployee assistance program"
        )

        self.stdout.write(self.style.SUCCESS(f"Created {created} directory jobs and updated {updated} benefits."))
