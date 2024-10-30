from unittest.mock import patch, MagicMock
from django.test import TestCase
from datetime import date, timedelta
from .tasks import sync_dashboard_data  # Adjust to your actual import path
from .models import DashboardEvent

class SyncDashboardDataTests(TestCase):
    @patch('base.tasks.requests.get')  # Mock the requests.get call
    @patch('base.models.DashboardEvent.objects.bulk_create')  # Mock database operation
    def test_sync_dashboard_data(self, mock_bulk_create, mock_get):
        # Set up mock response data for the requests.get call
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "id": "123",
                "status": 1,
                "hotel_id": "hotel_1",
                "room_id": "room_101",
                "night_of_stay": "2024-01-01",
                "timestamp": "2024-01-01T12:00:00Z"
            },
            {
                "id": "124",
                "status": 2,
                "hotel_id": "hotel_1",
                "room_id": "room_102",
                "night_of_stay": "2024-01-02",
                "timestamp": "2024-01-01T12:00:00Z"
            }
        ]
        mock_get.return_value = mock_response

        # Call the function
        sync_dashboard_data("2024-01-01")

        # Assertions to check if requests.get was called with correct parameters
        yesterday = date.today() - timedelta(days=1)
        mock_get.assert_called_once_with(
            'http://blankton_assesment-data_provider_service-1/events/',  # Replace with your actual URL
            params={'limit': 1000, 'offset': 0, 'updated_gte': "2024-01-01"}
        )

        # Check that bulk_create was called with DashboardEvent objects
        self.assertTrue(mock_bulk_create.called)
        # Check the arguments passed to bulk_create to ensure proper data structure
        created_events = mock_bulk_create.call_args[0][0]  # Access the list of objects passed to bulk_create

        # Validate the content of created objects
        self.assertEqual(len(created_events), 2)  # Should have created two objects
        self.assertEqual(created_events[0].hotel_id, "hotel_1")
        self.assertEqual(created_events[0].room_id, "room_101")
        self.assertEqual(created_events[0].night_of_stay,  "2024-01-01")
        self.assertEqual(created_events[0].rpg_status, DashboardEvent.BOOKING)

        # Print statements for debugging
        print(f"DashboardEvent bulk create calls: {mock_bulk_create.call_args}")
