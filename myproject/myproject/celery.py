import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Celery Beat schedule
app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'myapp.tasks.add',
        'schedule': 30.0,
        'args': (16, 16),
    },
    'run-every-midnight': {
        'task': 'myapp.tasks.scheduled_task',
        'schedule': crontab(hour=0, minute=0),
        # 'schedule': 10.0,
    },
}
