from django.apps import AppConfig


class JobsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "jobs"

    def ready(self):
        # Seed jobs from JSON when the app starts (for Render deployment)
        import os
        if os.environ.get("RENDER"):  # Only seed on Render production
            try:
                from .views import seed_jobs_from_json
                seed_jobs_from_json()
            except Exception:
                pass  # Database might not be ready yet; seeding will happen on first request
