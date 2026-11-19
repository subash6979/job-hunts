"""Generate expanded jobs.json with 5-9 jobs per country per sector."""
import json
import random
from pathlib import Path

random.seed(42)

COUNTRIES = [
    {"country": "Canada", "cities": ["Toronto", "Vancouver", "Montreal", "Ottawa", "Calgary", "Edmonton"]},
    {"country": "United States", "cities": ["New York", "San Francisco", "Seattle", "Chicago", "Austin", "Boston", "Los Angeles", "Washington, DC"]},
    {"country": "Nepal", "cities": ["Kathmandu", "Lalitpur", "Pokhara", "Biratnagar", "Bharatpur", "Butwal"]},
    {"country": "Japan", "cities": ["Tokyo", "Osaka", "Kyoto", "Yokohama", "Nagoya", "Fukuoka"]},
    {"country": "South Korea", "cities": ["Seoul", "Busan", "Incheon", "Daegu", "Daejeon", "Jeju"]},
    {"country": "Ireland", "cities": ["Dublin", "Cork", "Galway", "Limerick", "Waterford", "Kilkenny"]},
    {"country": "United Kingdom", "cities": ["London", "Manchester", "Birmingham", "Edinburgh", "Glasgow", "Bristol", "Leeds"]},
    {"country": "Germany", "cities": ["Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne", "Dusseldorf", "Stuttgart"]},
    {"country": "India", "cities": ["Mumbai", "Bengaluru", "New Delhi", "Hyderabad", "Chennai", "Pune", "Kolkata"]},
    {"country": "China", "cities": ["Beijing", "Shanghai", "Shenzhen", "Guangzhou", "Hangzhou", "Chengdu", "Hong Kong"]},
    {"country": "Hong Kong", "cities": ["Central and Western", "Wan Chai", "Kowloon", "Sha Tin", "Tuen Mun"]},
]

SECTORS = [
    "Healthcare",
    "IT & Technology",
    "Skilled Trades",
    "Transportation",
    "Education",
    "Hospitality & Retail",
]

JOBS_PER_COMBO = 7

SECTOR_JOBS = {
    "IT & Technology": [
        ("Software Engineer", ["Bachelor's degree in Computer Science", "Proficiency in Python and JavaScript", "Experience with React or Django", "Strong problem-solving skills", "Knowledge of REST APIs and databases"]),
        ("Web Developer", ["Proficiency in HTML, CSS, and JavaScript", "Experience with React, Vue, or Angular", "Understanding of responsive design", "Familiarity with version control (Git)", "Basic knowledge of backend development"]),
        ("Data Scientist", ["Degree in Statistics, Mathematics, or Data Science", "Proficiency in Python and SQL", "Experience with machine learning libraries", "Strong statistical analysis skills", "Ability to communicate data insights"]),
        ("DevOps Engineer", ["Experience with CI/CD pipelines", "Proficiency in Docker and Kubernetes", "Knowledge of cloud platforms (AWS/Azure/GCP)", "Scripting skills in Bash or Python", "Infrastructure-as-code experience"]),
        ("Cybersecurity Analyst", ["Understanding of network security protocols", "Experience with SIEM tools", "Knowledge of threat modeling and risk assessment", "Certification such as CompTIA Security+ or CISSP", "Incident response experience"]),
        ("Mobile App Developer", ["Proficiency in Swift or Kotlin", "Experience with React Native or Flutter", "Understanding of mobile UI/UX principles", "Experience publishing to app stores", "Knowledge of mobile security best practices"]),
        ("IT Support Specialist", ["Experience troubleshooting hardware and software", "Familiarity with Windows, macOS, and Linux", "Knowledge of networking fundamentals", "Strong customer service skills", "Experience with ticketing systems"]),
    ],
    "Healthcare": [
        ("Registered Nurse", ["Valid nursing license (RN)", "Bachelor's degree in Nursing or equivalent", "Experience in clinical patient care", "Strong communication and empathy", "BLS/ACLS certification"]),
        ("Medical Assistant", ["Certificate or diploma in Medical Assisting", "Knowledge of patient intake and vital signs", "Familiarity with electronic health records", "Phlebotomy skills preferred", "Strong organizational skills"]),
        ("Pharmacist", ["Doctor of Pharmacy (PharmD) degree", "Valid pharmacist license", "Knowledge of medications and drug interactions", "Attention to detail", "Strong counseling skills"]),
        ("Physical Therapist", ["Doctor of Physical Therapy (DPT) degree", "Valid physical therapy license", "Experience with patient rehabilitation", "Knowledge of anatomy and kinesiology", "Strong interpersonal skills"]),
        ("Dental Hygienist", ["Associate's degree in Dental Hygiene", "Valid dental hygiene license", "Experience with dental cleaning and prophylaxis", "Knowledge of oral health education", "Dexterity and attention to detail"]),
        ("Medical Lab Technician", ["Associate's degree in Clinical Laboratory Science", "Experience with laboratory testing and analysis", "Knowledge of lab safety protocols", "Attention to detail", "Ability to work with laboratory equipment"]),
        ("Healthcare Administrator", ["Bachelor's degree in Healthcare Administration", "Experience managing healthcare operations", "Knowledge of healthcare regulations", "Strong leadership skills", "Budgeting and scheduling experience"]),
    ],
    "Skilled Trades": [
        ("Electrician", ["Valid electrician license or apprenticeship", "Knowledge of electrical codes and safety", "Experience with wiring and troubleshooting", "Ability to read blueprints", "Physical stamina and dexterity"]),
        ("Plumber", ["Valid plumber license or apprenticeship", "Knowledge of pipe systems and codes", "Experience with installation and repair", "Ability to work in tight spaces", "Problem-solving skills"]),
        ("HVAC Technician", ["EPA certification preferred", "Experience with heating and cooling systems", "Knowledge of refrigeration principles", "Ability to diagnose system issues", "Customer service skills"]),
        ("Carpenter", ["Experience with framing and finish carpentry", "Ability to read blueprints", "Proficiency with hand and power tools", "Attention to detail", "Physical stamina"]),
        ("Welder", ["Welding certification (AWS or equivalent)", "Experience with MIG, TIG, or stick welding", "Knowledge of metallurgy and safety", "Ability to read welding symbols", "Steady hand and attention to detail"]),
        ("Automotive Technician", ["ASE certification preferred", "Experience with vehicle diagnostics and repair", "Knowledge of engine and brake systems", "Proficiency with diagnostic tools", "Strong problem-solving skills"]),
        ("Construction Worker", ["Experience with construction sites", "Knowledge of safety protocols", "Ability to operate hand and power tools", "Physical stamina and teamwork", "OSHA certification preferred"]),
    ],
    "Transportation": [
        ("Truck Driver", ["Commercial Driver's License (CDL)", "Clean driving record", "Experience with long-haul or regional driving", "Knowledge of DOT regulations", "Physical stamina for loading/unloading"]),
        ("Delivery Driver", ["Valid driver's license", "Clean driving record", "Experience with route planning", "Knowledge of local area", "Time management skills"]),
        ("Bus Driver", ["Commercial Driver's License with passenger endorsement", "Clean driving record", "Experience transporting passengers", "Customer service skills", "Knowledge of traffic laws"]),
        ("Logistics Coordinator", ["Bachelor's degree in Logistics or Supply Chain", "Experience with transportation management", "Knowledge of freight and shipping", "Strong organizational skills", "Proficiency with logistics software"]),
        ("Warehouse Associate", ["Experience with warehouse operations", "Ability to operate forklift (certification preferred)", "Knowledge of inventory management", "Physical stamina", "Attention to detail"]),
        ("Forklift Operator", ["Forklift certification", "Experience operating forklifts in warehouse", "Knowledge of safety protocols", "Ability to load and unload materials", "Attention to detail"]),
        ("Supply Chain Analyst", ["Bachelor's degree in Supply Chain or Business", "Experience with data analysis and forecasting", "Knowledge of inventory optimization", "Proficiency with Excel and ERP systems", "Strong analytical skills"]),
    ],
    "Education": [
        ("Elementary Teacher", ["Bachelor's degree in Education", "Valid teaching license/certification", "Experience with elementary curriculum", "Classroom management skills", "Patience and communication skills"]),
        ("High School Teacher", ["Bachelor's degree in subject area", "Valid teaching license/certification", "Experience with secondary curriculum", "Lesson planning skills", "Subject matter expertise"]),
        ("Professor", ["Master's or PhD in relevant field", "Experience in higher education teaching", "Research publication record", "Curriculum development skills", "Student mentoring experience"]),
        ("Tutor", ["Bachelor's degree or equivalent", "Experience tutoring students", "Strong subject knowledge", "Patience and ability to explain concepts", "Flexible scheduling"]),
        ("School Administrator", ["Master's degree in Education Administration", "Experience in school leadership", "Knowledge of education policies", "Budget and staff management", "Strong communication skills"]),
        ("Librarian", ["Master's degree in Library Science", "Experience with library operations", "Knowledge of cataloging and reference", "Customer service skills", "Organization and attention to detail"]),
        ("Special Education Teacher", ["Bachelor's degree in Special Education", "Valid special education certification", "Experience with IEPs and differentiated instruction", "Patience and empathy", "Collaboration skills with families and staff"]),
    ],
    "Hospitality & Retail": [
        ("Hotel Manager", ["Bachelor's degree in Hospitality Management", "Experience in hotel operations", "Staff management and scheduling", "Customer service excellence", "Budget and revenue management"]),
        ("Restaurant Server", ["Experience in food service", "Knowledge of food safety and hygiene", "Strong customer service skills", "Ability to work in fast-paced environment", "Cash handling experience"]),
        ("Front Desk Associate", ["Experience in hospitality or customer service", "Knowledge of reservation systems", "Strong communication skills", "Professional appearance and demeanor", "Multitasking ability"]),
        ("Retail Sales Associate", ["Experience in retail sales", "Knowledge of products and merchandising", "Strong customer service skills", "Cash handling and POS experience", "Ability to work flexible hours"]),
        ("Chef", ["Culinary school degree or equivalent", "Experience in professional kitchen", "Knowledge of food preparation and safety", "Menu planning skills", "Leadership and time management"]),
        ("Housekeeping", ["Experience in cleaning and housekeeping", "Attention to detail", "Knowledge of cleaning chemicals and equipment", "Physical stamina", "Time management skills"]),
        ("Customer Service Representative", ["Experience in customer service or call center", "Strong communication and listening skills", "Proficiency with CRM software", "Patience and problem-solving", "Ability to handle difficult customers"]),
    ],
}

COMPANY_PREFIXES = {
    "Canada": ["NorthStar", "MapleLeaf", "Canuck", "TrueNorth", "GreatWhite"],
    "United States": ["Liberty", "Eagle", "Starline", "Crossroads", "Allied"],
    "Nepal": ["Himalaya", "Everest", "Gorkha", "Kathmandu", "Sagarmatha"],
    "Japan": ["Sakura", "Nippon", "RisingSun", "Tokyo", "Fuji"],
    "South Korea": ["Seoul", "HanRiver", "Korea", "Gangnam", "Busan"],
    "Ireland": ["Shamrock", "Emerald", "Celtic", "Dublin", "Liffey"],
    "United Kingdom": ["Royal", "Union", "Brit", "London", "Meridian"],
    "Germany": ["Deutsche", "Berlin", "Bavaria", "Rhine", "Hanseatic"],
    "India": ["Taj", "Ganga", "Delhi", "Monsoon", "Spice"],
    "China": ["Dragon", "Yangtze", "Peking", "Silk", "GreatWall"],
    "Hong Kong": ["Pearl", "Harbor", "Dragon", "Kowloon", "Victoria"],
}

COMPANY_SUFFIXES = {
    "IT & Technology": ["Technologies", "Solutions", "Systems", "Labs", "Digital", "Softworks", "Cloud"],
    "Healthcare": ["Health", "Care", "Medical", "Clinic", "Wellness", "Medi", "Hospital"],
    "Skilled Trades": ["Build", "Craft", "Trade", "Works", "Pro", "Fix", "Builders"],
    "Transportation": ["Transit", "Logistics", "Freight", "Cargo", "Move", "Haul", "Fleet"],
    "Education": ["Learning", "Academy", "School", "Tutor", "Edu", "Scholar", "Teach"],
    "Hospitality & Retail": ["Hospitality", "Retail", "Mart", "Stay", "Serve", "Shop", "Guest"],
}


def random_company(country, sector):
    prefix = random.choice(COMPANY_PREFIXES[country])
    suffix = random.choice(COMPANY_SUFFIXES[sector])
    return f"{prefix} {suffix}"


def random_salary(sector):
    base = {
        "IT & Technology": (55000, 140000),
        "Healthcare": (45000, 130000),
        "Skilled Trades": (40000, 100000),
        "Transportation": (35000, 90000),
        "Education": (38000, 95000),
        "Hospitality & Retail": (30000, 75000),
    }[sector]
    lo, hi = base
    return f"${random.randint(lo // 1000, hi // 1000)}k - ${random.randint(lo // 1000 + 10, hi // 1000 + 20)}k"


def generate_jobs():
    jobs = []
    job_id = 1
    arrangements = ["remote", "hybrid", "on-site"]
    employment_types = ["full-time", "part-time", "contract", "internship"]
    experience_levels = ["entry-level", "mid-level", "senior"]
    posted_dates = ["2026-01-10", "2026-02-15", "2026-03-20", "2026-04-25", "2026-05-30", "2026-06-12", "2026-07-18"]

    for country_data in COUNTRIES:
        country = country_data["country"]
        cities = country_data["cities"]
        for sector in SECTORS:
            job_templates = SECTOR_JOBS[sector]
            sampled_templates = random.sample(job_templates, len(job_templates))[:JOBS_PER_COMBO]
            for i in range(JOBS_PER_COMBO):
                title, requirements = sampled_templates[i % len(sampled_templates)]
                city = random.choice(cities)
                company = random_company(country, sector)
                description = (
                    f"We are seeking a {title} to join our team at {company} in {city}, {country}. "
                    f"This is a great opportunity for a motivated professional to contribute to our growing organization."
                )
                benefits = random.sample([
                    "Health insurance", "Paid time off", "Retirement plan", "Flexible hours",
                    "Professional development", "Remote work options", "Employee discounts", "Life insurance"
                ], k=random.randint(2, 4))
                job = {
                    "id": job_id,
                    "title": title,
                    "company": company,
                    "location": f"{city}, {country}",
                    "country": country,
                    "city": city,
                    "category": sector,
                    "description": description,
                    "requirements": requirements,
                    "salary": random_salary(sector),
                    "workArrangement": random.choice(arrangements),
                    "employmentType": random.choice(employment_types),
                    "experienceLevel": random.choice(experience_levels),
                    "benefits": benefits,
                    "companyVerified": random.choice([True, False, False]),
                    "applyLink": f"https://www.{company.lower().replace(' ', '')}.com/careers/{title.lower().replace(' ', '-')}",
                    "postedDate": random.choice(posted_dates),
                }
                jobs.append(job)
                job_id += 1

    return jobs


if __name__ == "__main__":
    jobs = generate_jobs()
    out_path = Path(__file__).resolve().parent / "data" / "jobs.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)
    print(f"Generated {len(jobs)} jobs across {len(COUNTRIES)} countries and {len(SECTORS)} sectors -> {out_path}")