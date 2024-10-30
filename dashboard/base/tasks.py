import requests
import logging
from celery import shared_task
from requests import RequestException
from .models import DashboardEvent
from datetime import date, timedelta

logger = logging.getLogger(__name__)

DATA_PROVIDER_URL = 'http://blankton_assesment-data_provider_service-1/events/'

@shared_task(name="sync_dashboard_data")
def sync_dashboard_data(updated_gte: str):
    # Example of fetching data from Data Provider's GET /events endpoint
    yesterday = date.today() - timedelta(days=1)
    response = requests.get(DATA_PROVIDER_URL, params={'limit': 1000, 'offset': 0, 'updated_gte': updated_gte})
    if response.status_code == 200:
        events = response.json()
        # Process events and update DailyBooking and MonthlyBooking models accordingly
        dashboard_events = []
        for event in events:
            # Parse the event data and update the models
            # Create a DashboardEvent instance but don't save it yet
            dashboard_event = DashboardEvent(
                id=event["id"],
                room_id=event["room_id"],
                night_of_stay=event["night_of_stay"],
                rpg_status=event["status"],
                timestamp=event["timestamp"],
                hotel_id=event["hotel_id"]
            )
            dashboard_events.append(dashboard_event)
        if dashboard_events:
            DashboardEvent.objects.bulk_create(dashboard_events)
            logger.info("sync task complete!!!")
    else:
        logger.error("Error in sync_dashboard_data() task")
        raise Exception("Error in sync_dashboard_data() task: " + str(response))
    
@shared_task(name="test_celery_task")
def test_celery_task():
    logger.debug("Testing celery task is good")
    return "Hello, task from celery!"
