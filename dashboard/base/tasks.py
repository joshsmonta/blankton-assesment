import requests
import logging
from celery import shared_task
from django.db import transaction
from .models import DashboardEvent
from dashboard_service.settings import DATA_PROVIDER_URL
from datetime import date, timedelta

logger = logging.getLogger(__name__)

event_url = f"{DATA_PROVIDER_URL}/events/" 
# event_url = "http://192.168.128.3:8000/events/"
# event_url = "http://127.0.0.1:8000/events/"
@shared_task(name="sync_dashboard_data")
def sync_dashboard_data(updated_gte: str):
    try:
        # Step 1: Fetch data from the Data Provider API with filtering
        if not updated_gte or updated_gte == '':
            yesterday = date.today() - timedelta(days=1)
            updated_gte = yesterday.strftime('%Y-%m-%d')
        response = requests.get(event_url, params={'updated_gte': updated_gte})
        
        # Check the response status
        response.raise_for_status()  # Raises an error for bad responses (4xx and 5xx)

        # Attempt to parse the response as JSON
        try:
            events = response.json()
        except ValueError as e:
            logger.error(f"JSON decode error: {str(e)} | Response text: {response.text}")
            return  # Exit if JSON decoding fails

        # Step 2: Extract IDs and query for existing records
        event_ids = [event["id"] for event in events if "id" in event]  # Safely access "id"
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
        # batch_size = 1000
        if dashboard_events:
            DashboardEvent.objects.bulk_create(dashboard_events)
            logger.info("Sync task complete: %d new events added.", len(dashboard_events))
        else:
            logger.info("No new events to add.")
    except requests.RequestException as e:
        logger.error(f"Request error: {str(e)}")
    except Exception as e:
        logger.error(f"An error occurred in sync_dashboard_data: {str(e)}")

    
@shared_task(name="test_celery_task")
def test_celery_task():
    logger.debug("Testing celery task is good")
    return "Hello, task from celery!"
