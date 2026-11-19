import json
from pathlib import Path

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.conf import settings
from django.http import FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Application, Job, UserSettings


def home(request):
    seed_jobs_from_json()
    return FileResponse((Path(settings.BASE_DIR) / "index.html").open("rb"))


@require_http_methods(["GET"])
def jobs(request):
    seed_jobs_from_json()
    queryset = Job.objects.all()
    search = request.GET.get("q", "").strip()
    country = request.GET.get("country", "").strip()
    city = request.GET.get("city", "").strip()
    arrangement = request.GET.get("work_arrangement", "").strip()
    employment_type = request.GET.get("employment_type", "").strip()
    category = request.GET.get("category", "").strip()
    if search:
        queryset = queryset.filter(title__icontains=search) | queryset.filter(company__icontains=search) | queryset.filter(description__icontains=search)
    if country:
        queryset = queryset.filter(country__iexact=country)
    if city:
        queryset = queryset.filter(city__iexact=city) | queryset.filter(location__icontains=city)
    if arrangement:
        queryset = queryset.filter(work_arrangement=arrangement)
    if employment_type:
        queryset = queryset.filter(employment_type=employment_type)
    if category:
        queryset = queryset.filter(category__iexact=category)
    return JsonResponse([job.to_dict() for job in queryset], safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Request body must be valid JSON."}, status=400)

    username = (payload.get("username") or payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""
    if not username or not email or not password:
        return JsonResponse({"error": "Username, email, and password are required."}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "That username is already in use."}, status=409)
    if User.objects.filter(email=email).exists():
        return JsonResponse({"error": "That email is already registered."}, status=409)

    user = User.objects.create_user(username=username, email=email, password=password)
    return JsonResponse({"id": user.id, "username": user.username}, status=201)


@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Request body must be valid JSON."}, status=400)

    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""
    user = User.objects.filter(email=email).first()
    authenticated_user = authenticate(
        request, username=user.username if user else "", password=password
    )
    if authenticated_user is None:
        return JsonResponse({"error": "Invalid email or password."}, status=401)

    login(request, authenticated_user)
    return JsonResponse({"id": authenticated_user.id, "username": authenticated_user.username})


@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Logged out."})


@csrf_exempt
@require_http_methods(["POST"])
def post_job(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "You must be logged in to post a job."}, status=401)
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Request body must be valid JSON."}, status=400)

    required_fields = {
        "title": payload.get("title"),
        "company": payload.get("company"),
        "location": payload.get("location"),
        "description": payload.get("description"),
    }
    if any(not str(value or "").strip() for value in required_fields.values()):
        return JsonResponse({"error": "Title, company, location, and description are required."}, status=400)

    requirements = payload.get("requirements", "")
    if isinstance(requirements, list):
        requirements = "\n".join(str(item) for item in requirements)
    job = Job.objects.create(
        title=required_fields["title"].strip(),
        company=required_fields["company"].strip(),
        location=required_fields["location"].strip(),
        category=str(payload.get("category", "IT & Technology")).strip(),
        country=str(payload.get("country", "United States")).strip(),
        city=str(payload.get("city", "")).strip(),
        work_arrangement=str(payload.get("workArrangement", "on-site")).strip(),
        employment_type=str(payload.get("employmentType", "full-time")).strip(),
        experience_level=str(payload.get("experienceLevel", "mid-level")).strip(),
        salary_min=payload.get("salaryMin") or None,
        salary_max=payload.get("salaryMax") or None,
        salary_currency=str(payload.get("salaryCurrency", "USD")).strip().upper(),
        description=required_fields["description"].strip(),
        requirements=str(requirements).strip(),
        benefits="\n".join(str(item) for item in payload.get("benefits", [])) if isinstance(payload.get("benefits", []), list) else str(payload.get("benefits", "")).strip(),
        salary=str(payload.get("salary", "")).strip(),
        apply_link=str(payload.get("applyLink", "")).strip(),
        posted_by=request.user,
    )
    return JsonResponse(job.to_dict(), status=201)


@require_http_methods(["GET"])
def me(request):
    if not request.user.is_authenticated:
        return JsonResponse({"authenticated": False})
    return JsonResponse({
        "authenticated": True,
        "id": request.user.id,
        "username": request.user.username,
        "email": request.user.email,
    })


@csrf_exempt
@require_http_methods(["POST"])
def apply(request, job_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Log in before applying."}, status=401)
    job = Job.objects.filter(id=job_id).first()
    if job is None:
        return JsonResponse({"error": "Job not found."}, status=404)
    application = Application.objects.create(
        job=job,
        candidate=request.user,
        resume=request.FILES.get("resume"),
        cover_note=request.POST.get("cover_note", ""),
    )
    return JsonResponse({"id": application.id, "status": application.status}, status=201)


@require_http_methods(["GET"])
def applications(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Log in to view applications."}, status=401)
    records = Application.objects.filter(candidate=request.user).select_related("job")
    return JsonResponse([
        {"id": item.id, "jobTitle": item.job.title, "company": item.job.company, "status": item.status, "updatedAt": item.updated_at.isoformat()}
        for item in records
    ], safe=False)


@require_http_methods(["GET", "PATCH"])
def settings_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Log in to manage settings."}, status=401)
    preferences, _ = UserSettings.objects.get_or_create(user=request.user)
    if request.method == "PATCH":
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Request body must be valid JSON."}, status=400)
        for field in ("email_job_alerts", "email_application_updates", "email_product_updates"):
            if field in payload:
                setattr(preferences, field, bool(payload[field]))
        preferences.save()
    return JsonResponse({
        "emailJobAlerts": preferences.email_job_alerts,
        "emailApplicationUpdates": preferences.email_application_updates,
        "emailProductUpdates": preferences.email_product_updates,
        "googleConnected": preferences.google_connected,
    })


@csrf_exempt
@require_http_methods(["POST"])
def change_password(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Log in to change your password."}, status=401)
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Request body must be valid JSON."}, status=400)
    if not request.user.check_password(payload.get("currentPassword", "")):
        return JsonResponse({"error": "Current password is incorrect."}, status=400)
    new_password = payload.get("newPassword", "")
    if len(new_password) < 8:
        return JsonResponse({"error": "New password must be at least 8 characters."}, status=400)
    request.user.set_password(new_password)
    request.user.save(update_fields=["password"])
    update_session_auth_hash(request, request.user)
    return JsonResponse({"message": "Password updated."})


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_account(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Log in to delete your account."}, status=401)
    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        payload = {}
    if payload.get("confirmation") != "DELETE":
        return JsonResponse({"error": "Type DELETE to confirm account deletion."}, status=400)
    user = request.user
    logout(request)
    user.delete()
    return JsonResponse({"message": "Account deleted."})


def seed_jobs_from_json():
    data_path = Path(__file__).resolve().parent.parent / "data" / "jobs.json"
    if not data_path.exists():
        return
    with data_path.open(encoding="utf-8") as data_file:
        seed_data = json.load(data_file)
    for item in seed_data:
        Job.objects.update_or_create(
            id=item["id"],
            defaults={
                "title": item["title"],
                "company": item["company"],
                "location": item["location"],
                "country": item.get("country", ""),
                "city": item.get("city", ""),
                "category": item.get("category", "IT & Technology"),
                "work_arrangement": item.get("workArrangement", "on-site"),
                "employment_type": item.get("employmentType", "full-time"),
                "experience_level": item.get("experienceLevel", "mid-level"),
                "description": item["description"],
                "requirements": "\n".join(item.get("requirements", [])),
                "benefits": "\n".join(item.get("benefits", [])),
                "salary": item.get("salary", ""),
                "apply_link": item.get("applyLink", ""),
                "company_verified": item.get("companyVerified", False),
            },
        )
