from django.urls import path
from .views import (
    CreateCompanyView,
    CompanyListAPIView,
    ProjectView,
    ListProjectAPIsView,
    EnvironmentView,
    ProjectLogsAPIView
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
        "projects/<str:id>",
        ProjectView.as_view(),
        name="create project",
    ),
    # api
    path(
        "apis/<str:id>",
        ListProjectAPIsView.as_view(),
        name="List all API's of a project",
    ),
    path(
        "envs/<str:id>",
        EnvironmentView.as_view(),
        name="List all envs of a company",
    ),
    path(
        "projects/<str:id>/logs",
        ProjectLogsAPIView.as_view(),
        name="List paginated api logs of a project",
    )

]
