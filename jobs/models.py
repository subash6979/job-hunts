from django.conf import settings
from django.db import models


class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=100, default="IT & Technology")
    country = models.CharField(max_length=100, default="United States")
    city = models.CharField(max_length=100, blank=True)
    work_arrangement = models.CharField(
        max_length=20,
        choices=[("remote", "Remote"), ("hybrid", "Hybrid"), ("on-site", "On-site")],
        default="on-site",
    )
    employment_type = models.CharField(
        max_length=20,
        choices=[("full-time", "Full-time"), ("part-time", "Part-time"), ("contract", "Contract"), ("temporary", "Temporary"), ("internship", "Internship")],
        default="full-time",
    )
    experience_level = models.CharField(
        max_length=20,
        choices=[("entry-level", "Entry level"), ("mid-level", "Mid level"), ("senior", "Senior")],
        default="mid-level",
    )
    salary_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_currency = models.CharField(max_length=3, default="USD")
    company_verified = models.BooleanField(default=False)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    benefits = models.TextField(blank=True)
    salary = models.CharField(max_length=100, blank=True)
    apply_link = models.URLField(blank=True)
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posted_jobs",
    )
    posted_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-posted_date", "-id"]

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "category": self.category,
            "country": self.country,
            "city": self.city,
            "workArrangement": self.work_arrangement,
            "employmentType": self.employment_type,
            "experienceLevel": self.experience_level,
            "description": self.description,
            "requirements": [
                item.strip() for item in self.requirements.splitlines() if item.strip()
            ],
            "benefits": [item.strip() for item in self.benefits.splitlines() if item.strip()],
            "salary": self.salary,
            "salaryMin": self.salary_min,
            "salaryMax": self.salary_max,
            "salaryCurrency": self.salary_currency,
            "companyVerified": self.company_verified,
            "postedDate": self.posted_date.isoformat(),
            "applyLink": self.apply_link,
        }


class Application(models.Model):
    STATUS_CHOICES = [
        ("submitted", "Submitted"),
        ("reviewing", "Reviewing"),
        ("interview", "Interview"),
        ("offer", "Offer"),
        ("rejected", "Rejected"),
        ("hired", "Hired"),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    resume = models.FileField(upload_to="resumes/", blank=True)
    cover_note = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="submitted")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]


class UserSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="settings")
    email_job_alerts = models.BooleanField(default=True)
    email_application_updates = models.BooleanField(default=True)
    email_product_updates = models.BooleanField(default=False)
    google_connected = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
