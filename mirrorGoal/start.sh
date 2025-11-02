#!/bin/bash

# Start Celery Worker in background
celery -A mirrorGoal worker --loglevel=info --pool=solo &

# Start Celery Beat in background
celery -A mirrorGoal beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler &

# Start Django with Daphne (foreground)
daphne -b 0.0.0.0 -p $PORT mirrorGoal.asgi:application
