from django.apps import AppConfig
# from django_celery_beat.models import PeriodicTask, IntervalSchedule
# from datetime import timedelta


class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'

# # Set up interval schedule for daily execution
# schedule, _ = IntervalSchedule.objects.get_or_create(
#     every=1,
#     period=IntervalSchedule.DAYS,
# )

# # Register the periodic task
# PeriodicTask.objects.create(
#     interval=schedule,
#     name='Sync Dashboard Data',
#     task='tasks.sync_dashboard_data',
# )