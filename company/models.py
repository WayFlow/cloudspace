from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=50, unique=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="get_user_companies"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.company_name


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="get_company_projects"
    )
    mongo_connection_uri = models.TextField(null=True)

    def __str__(self) -> str:
        return self.project_name
