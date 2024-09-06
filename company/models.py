import uuid

from django.contrib.auth import get_user_model
from django.db import models
from utils.crypto import generate_secret_key

User = get_user_model()


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=50, unique=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="get_user_companies"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self) -> str:
        return self.company_name


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    secret_key = models.CharField(max_length=255, default=generate_secret_key)
    project_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="get_company_projects"
    )

    def __str__(self) -> str:
        return self.project_name


class ProjectEnvironment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    env = models.CharField(max_length=30)



class CompanySecret(models.Model):

    class SecretType(models.Choices):
        DATABASE_TYPE = "database_secret"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=30, default=SecretType.DATABASE_TYPE, choices=SecretType.choices)
    db_name = models.CharField(max_length=120)
    public_key = models.CharField(max_length=120)
    private_key = models.CharField(max_length=120)
    db_project_id = models.CharField(max_length=120)
    cluster_name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    env = models.ForeignKey(ProjectEnvironment, on_delete=models.SET_NULL, null=True, related_name='get_env_secrets')
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="get_company_secrets"
    )



class DBSchema(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    db_name = models.CharField(max_length=255)
    current_schema = models.JSONField()
    last_schema = models.JSONField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="get_db_details"
    )
