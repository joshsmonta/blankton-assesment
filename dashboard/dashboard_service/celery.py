import django
import os
from __future__ import absolute_import, unicode_literals
from celery import Celery
from django.conf import settings
django.setup()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard_service.settings')
app = Celery('dashboard_service')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
