import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dateapp.settings')

app = Celery('dateapp')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'refresh_people_12h': {
        'task': 'profiles.tasks.refresh_people',
        'schedule': 43200.0  # 12 hours, 12 * 60 * 60
    }
}

app.autodiscover_tasks()