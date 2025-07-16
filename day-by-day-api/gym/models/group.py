from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    meta_semanal_padrao = models.IntegerField(default=5) 
    
    def __str__(self):
        return self.name