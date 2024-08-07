from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='get_user_companies')
