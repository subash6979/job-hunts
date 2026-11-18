from django.conf import settings
from django.urls import include, path, re_path
from django.views.static import serve

from jobs import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/", include("jobs.urls")),
    re_path(r"^(?P<path>.*)$", serve, {"document_root": settings.BASE_DIR}),
]
