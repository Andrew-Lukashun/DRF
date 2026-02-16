import os

from celery import Celery

os.environ.setdefault(key="DJANGO_SETTINGS_MODULE", value="config.settings")

app = Celery("config")
app.config_from_object(obj="django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
