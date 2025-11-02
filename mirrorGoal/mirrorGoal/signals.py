from django.dispatch import receiver
from django.db.models.signals import post_save
from mirrorGoal.models import User, NotificationSetting, ProgressHistory, CheckIn

@receiver(post_save, sender=User)
def create_notification_settings(sender, instance, created, **kwargs):
    if created:
        for notif_type, _ in NotificationSetting.NOTIFICATION_TYPES:
            NotificationSetting.objects.create(user=instance, type=notif_type)