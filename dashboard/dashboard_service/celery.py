import django
import os
from celery import Celery
from kombu import Queue
from .settings import CELERY_BROKER_URL

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard_service.settings')
app = Celery('dashboard_service')
app.autodiscover_tasks()
app.conf.broker_url = CELERY_BROKER_URL
app.conf.result_backend = CELERY_BROKER_URL
app.conf.accept_content = ["application/json"]
app.conf.task_serializer = "json"
app.conf.result_serializer = "json"
app.conf.task_default_queue = "default"
app.conf.task_create_missing_queues = True
app.conf.broker_connection_retry_on_startup = True
app.conf.task_queues = (Queue("default"),)
app.conf.broker_connection_timeout = 30
app.conf.worker_prefetch_multiplier = 1
app.conf.redbeat_redis_url = CELERY_BROKER_URL

