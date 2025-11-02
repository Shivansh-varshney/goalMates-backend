from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import Goal, CheckIn

@shared_task
def update_all_goal_progress():
    active_goals = Goal.objects.filter(status="Active")
    for goal in active_goals:
        goal.update_progress()

@shared_task
def mark_missed_checkins():
    grace_time = timezone.now() - timedelta(minutes=15)
    missed_checkins = CheckIn.objects.filter(checked_in_at__isnull=True, scheduled_for__lt=grace_time)

    for checkin in missed_checkins:
        goal = checkin.goal
        goal.reset_goal()
        checkin.missed = True
        checkin.save()