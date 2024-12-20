from django.urls import path
from .views import (
    CreateCompanyView,
    CompanyListAPIView,
    ProjectView,
    ListProjectAPIsView,
    EnvironmentView,
    ProjectLogsAPIView,
    DBSecretView
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
        "cmp/<str:id>/projects",
        ProjectView.as_view(),
        name="create project or get projects",
    ),
    path(
        "cmp/<str:id>/envs",
        EnvironmentView.as_view(),
        name="List all envs of a company",
    ),
    # api
    path(
        "project/<str:id>/apis",
        ListProjectAPIsView.as_view(),
        name="List all API's of a project create",
    ),
    path(
        "project/<str:id>/logs",
        ProjectLogsAPIView.as_view(),
        name="List paginated api logs of a project",
    ),
    path(
        "project/<str:id>/secrets",
        DBSecretView.as_view(),
        name="List and create secrets of a project",
    )

]
