from django.contrib.auth.models import AbstractUser
from django.db import models

class UserDay(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    goals = models.CharField(blank=True, null=True)