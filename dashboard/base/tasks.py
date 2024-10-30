import requests
import logging
from celery import shared_task
from django.db import transaction
from requests import RequestException
from .models import DashboardEvent
from datetime import date, timedelta

logger = logging.getLogger(__name__)

DATA_PROVIDER_URL = 'http://blankton_assesment-data_provider_service-1:8000/events/'
# DATA_PROVIDER_URL = 'http://127.0.0.1:8000/events/'


@shared_task(name="sync_dashboard_data")
def sync_dashboard_data(updated_gte: str):
    # Step 1: Fetch data from the Data Provider API with filtering if possible
    response = requests.get(DATA_PROVIDER_URL, params={'limit': 10000, 'offset': 0, 'updated_gte': updated_gte})
    if response.status_code == 200:
        events = response.json()

        # Step 2: Extract IDs and query for existing records in batches if very large
        event_ids = [event["id"] for event in events]
        existing_ids = set(DashboardEvent.objects.filter(id__in=event_ids).values_list('id', flat=True))

        # Step 3: Prepare new DashboardEvent instances
        dashboard_events = [
            DashboardEvent(
                id=event["id"],
                room_id=event["room_id"],
                night_of_stay=event["night_of_stay"],
                rpg_status=event["rpg_status"],
                timestamp=event["timestamp"],
                hotel_id=event["hotel_id"]
            )
            for event in events if event["id"] not in existing_ids
        ]

        # Step 4: Batch insert new records to optimize database performance
        batch_size = 1000
        if dashboard_events:
            with transaction.atomic():
                DashboardEvent.objects.bulk_create(dashboard_events, batch_size=batch_size)
            logger.info("sync task complete!!!")
    else:
        logger.error("Error in sync_dashboard_data() task")
        raise Exception("Error in sync_dashboard_data() task: " + str(response))

    
@shared_task(name="test_celery_task")
def test_celery_task():
    logger.debug("Testing celery task is good")
    return "Hello, task from celery!"
