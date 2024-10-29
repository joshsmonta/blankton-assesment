from celery import shared_task
from requests import RequestException
import requests
from .models import DashboardEvent
from datetime import date, timedelta

DATA_PROVIDER_URL = 'http://127.0.0.1:8000/events/'

# @shared_task
def sync_dashboard_data():
    # Example of fetching data from Data Provider's GET /events endpoint
    yesterday = date.today() - timedelta(days=1)
    response = requests.get(DATA_PROVIDER_URL, params={'limit': 1000, 'offset': 0, 'updated_gte': yesterday.strftime('%Y-%m-%d')})
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
    else:
        # Handle error
        raise "Error in sync_dashboard_data() task"
        pass
