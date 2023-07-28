from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
    path("api/v1/", include("fifth_ed.urls")),
    path("social/", include("social_login.urls")),
    path("", include("social_django.urls", namespace="social")),
]
