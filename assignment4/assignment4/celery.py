from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set default Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assignment4.settings')

app = Celery('assignment4')

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks from installed apps
app.autodiscover_tasks()
