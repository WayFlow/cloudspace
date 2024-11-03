from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("c/", include("core.urls")),
    path("api/v1/auth/", include("account.urls")),
    path("api/v1/company/", include("company.urls")),
]
