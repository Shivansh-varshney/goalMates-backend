from django.apps import AppConfig

class MirrorGoalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mirrorGoal'

    def ready(self):
        import mirrorGoal.signals