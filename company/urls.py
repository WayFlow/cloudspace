from django.urls import path
from .views import (
    CreateCompanyView,
    CompanyListAPIView,
    ProjectView,
    ListAPIProjectView,
)

urlpatterns = [
    # company
    path(
        "create",
        CreateCompanyView.as_view(),
        name="create company",
    ),
    path(
        "list",
        CompanyListAPIView.as_view(),
        name="list company",
    ),
    # projects
    path(
        "projects",
        ProjectView.as_view(),
        name="create project",
    ),
    # api
    path(
        "apis/<str:id>",
        ListAPIProjectView.as_view(),
        name="List all API's of a project",
    ),
]
