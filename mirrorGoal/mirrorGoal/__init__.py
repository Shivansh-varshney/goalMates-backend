from .celery import app as celery_app

default_app_config = 'mirrorGoal.apps.MirrorGoalConfig'

__all__ = ("celery_app",)