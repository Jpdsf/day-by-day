from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model
from gym.models.group import Group
from gym.utils.calculations import calcular_streak_usuario

User = get_user_model()

class GroupMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    data_entrada = models.DateField(auto_now_add=True)
    meta_semanal_individual = models.IntegerField(null=True, blank=True)
    streak_atual = models.IntegerField(default=0)
    melhor_streak = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['user', 'group']
    
    @property
    def meta_semanal(self):
        return self.meta_semanal_individual or self.group.meta_semanal_padrao
    
    def calcular_streak(self):
        return calcular_streak_usuario(self.user, self.group, GroupMembership)