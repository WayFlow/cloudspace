import uuid

from django.contrib.auth import get_user_model
from django.db import models
from utils.crypto import generate_secret_key, generate_crc32_hash

User = get_user_model()


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=50, unique=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="get_user_companies"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(null=True, blank=True)
    route = models.CharField(max_length=8, editable=False, blank=True)

    def __str__(self) -> str:
        return self.company_name
    
    def save(self, *args, **kwargs):
        if not self.route and self.id:
            self.route = generate_crc32_hash(str(self.id))
        super(Company, self).save(*args, **kwargs)


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


class Environment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    env = models.CharField(max_length=30)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="get_company_envs")

# TODO: what is the use of this Table ?
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


class DBSecret(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    db_name = models.CharField(max_length=120)
    public_key = models.CharField(max_length=120)
    private_key = models.CharField(max_length=120)
    db_project_id = models.CharField(max_length=120)
    cluster_name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="get_db_secret"
    )
    env = models.ForeignKey(
        Environment, on_delete=models.CASCADE, related_name="get_env_secrets"
    )


class API(models.Model):

    class RequestMethod(models.TextChoices):
        GET="GET"
        POST="POST"
        PUT="PUT"
        DELETE="DELETE"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    method = models.CharField(max_length=10, choices=RequestMethod.choices)
    endpoint = models.TextField()
    query_params = models.JSONField(default=dict)
    request_body = models.JSONField(default=dict)
    authenticated = models.BooleanField(default=False)
    flow = models.CharField(max_length=120, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='get_project_apis')
