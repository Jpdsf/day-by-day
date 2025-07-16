from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from gym.models import WorkoutRecord, GroupMembership

@receiver(post_save, sender=WorkoutRecord)
def recalcular_streak_apos_treino(sender, instance, created, **kwargs):
    if created:
        membership = GroupMembership.objects.get(
            user=instance.user, 
            group=instance.group
        )
        membership.calcular_streak()

@receiver(post_delete, sender=WorkoutRecord)
def recalcular_streak_apos_remover_treino(sender, instance, **kwargs):
    try:
        membership = GroupMembership.objects.get(
            user=instance.user, 
            group=instance.group
        )
        membership.calcular_streak()
    except GroupMembership.DoesNotExist:
        pass