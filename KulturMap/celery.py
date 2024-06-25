# Celery Configuration
from celery import Celery
from celery.schedules import crontab
import os

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OpenDataEuskadi.settings')

app = Celery('OpenDataEuskadi')
app.conf.enable_utc = False
app.conf.update(timezone="Europe/Madrid")
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Define periodic tasks
app.conf.beat_schedule = {
    'telegram_bot': {
        'task': 'apps.automations.tasks.telegram_bot',
        'schedule': crontab(minute='5'),
    },
    'ingest_traffic_events': {
        'task': 'apps.automations.tasks.ingest_traffic_events',
        'schedule': crontab(minute='*/15'),
    },
    'ingest_culture_events': {
        'task': 'apps.automations.tasks.ingest_culture_events',
        'schedule': crontab(hour='20', minute='00'),
    },
    'ingest_culture_events_kids': {
        'task': 'apps.automations.tasks.ingest_culture_events_kids',
        'schedule': crontab(hour='0', minute='20'),
    },
    'ingest_culture_events_upcoming': {
        'task': 'apps.automations.tasks.ingest_culture_events_upcoming',
        'schedule': crontab(hour='1', minute='0'),
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
