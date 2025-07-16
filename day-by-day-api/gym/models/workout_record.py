from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from gym.models.group import Group
from gym.models.group_member_ship import GroupMembership

User = get_user_model()

class WorkoutRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    data_treino = models.DateField()
    exercicios = models.TextField(blank=True)
    observacoes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'group', 'data_treino']
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        membership = GroupMembership.objects.get(user=self.user, group=self.group)
        membership.calcular_streak()