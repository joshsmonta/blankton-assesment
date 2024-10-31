from unittest.mock import patch, MagicMock
from django.test import TestCase
from datetime import date, timedelta
from .tasks import sync_dashboard_data  # Adjust to your actual import path
from .models import DashboardEvent
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.core.management import call_command
from unittest.mock import patch
from rest_framework import status
from rest_framework.test import APIClient
from .models import DashboardEvent
from dashboard_service.settings import DATA_PROVIDER_URL

class DashboardViewTests(TestCase):
    def setUp(self):
        # Set up test data
        self.client = APIClient()
        self.hotel_id = 1
        self.year = timezone.now().year
        
        # Create sample data
        DashboardEvent.objects.bulk_create([
            DashboardEvent(id='1', hotel_id=self.hotel_id, room_id='101', night_of_stay='2024-01-01', rpg_status=1, timestamp=timezone.now()),
            DashboardEvent(id='2', hotel_id=self.hotel_id, room_id='102', night_of_stay='2024-01-01', rpg_status=2, timestamp=timezone.now()),
            DashboardEvent(id='3', hotel_id=self.hotel_id, room_id='101', night_of_stay='2024-01-02', rpg_status=1, timestamp=timezone.now()),
        ])

    def test_missing_parameters(self):
        """Test missing hotel_id, period, or year parameter"""
        response = self.client.get(reverse('dashboard'))  # URL for DashboardView
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('hotel_id, period, and year parameters are required', response.data['message'])

    def test_invalid_parameter_type(self):
        """Test hotel_id or year with invalid types"""
        response = self.client.get(reverse('dashboard'), {'hotel_id': 'abc', 'period': 'day', 'year': 'abc'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('hotel_id and year must be integers', response.data['message'])

    def test_invalid_period_value(self):
        """Test invalid period value"""
        response = self.client.get(reverse('dashboard'), {'hotel_id': self.hotel_id, 'period': 'invalid', 'year': self.year})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid period. Must be "day", "month", or "year".', response.data['message'])

    def test_dashboard_day_view(self):
        """Test dashboard data for 'day' period"""
        response = self.client.get(reverse('dashboard'), {'hotel_id': self.hotel_id, 'period': 'day', 'year': self.year})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))
        for item in response.data:
            self.assertIn('daily_bookings', item)
            self.assertIn('daily_cancellations', item)

    def test_dashboard_month_view(self):
        """Test dashboard data for 'month' period"""
        response = self.client.get(reverse('dashboard'), {'hotel_id': self.hotel_id, 'period': 'month', 'year': self.year})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))
        for item in response.data:
            self.assertIn('monthly_bookings', item)
            self.assertIn('monthly_cancellations', item)

    def test_dashboard_year_view(self):
        """Test dashboard data for 'year' period"""
        response = self.client.get(reverse('dashboard'), {'hotel_id': self.hotel_id, 'period': 'year', 'year': self.year})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))
        for item in response.data:
            self.assertIn('yearly_bookings', item)
            self.assertIn('yearly_cancellations', item)

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
                "rpg_status": 1,
                "hotel_id": "hotel_1",
                "room_id": "room_101",
                "night_of_stay": "2024-01-01",
                "timestamp": "2024-01-01T12:00:00Z"
            },
            {
                "id": "124",
                "rpg_status": 2,
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
        # data_url = "http://192.168.128.3:8000/events/"
        data_url = f"{DATA_PROVIDER_URL}/events/"
        yesterday = date.today() - timedelta(days=1)
        mock_get.assert_called_once_with(
            data_url,  # Replace with your actual URL
            params={'updated_gte': "2024-01-01"}
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
