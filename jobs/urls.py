from django.urls import path

from . import views

urlpatterns = [
    path("jobs/", views.jobs, name="jobs"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("post-job/", views.post_job, name="post-job"),
    path("me/", views.me, name="me"),
    path("jobs/<int:job_id>/apply/", views.apply, name="apply"),
    path("applications/", views.applications, name="applications"),
    path("settings/", views.settings_view, name="settings"),
    path("password/", views.change_password, name="change-password"),
    path("delete-account/", views.delete_account, name="delete-account"),
]
