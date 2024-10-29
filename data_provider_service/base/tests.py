from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Event
from django.utils.timezone import now, timedelta

class EventViewSetTests(TestCase):
    def setUp(self):
        # Set up a test client and create some events
        self.client = APIClient()
        self.url = '/events/'
        self.today = now().date()

        # Create some test events
        Event.objects.create(
            hotel_id=1,
            timestamp=now(),
            rpg_status=1,  # Booking
            room_id=101,
            night_of_stay=self.today,
            id=99999999
        )
        Event.objects.create(
            hotel_id=1,
            timestamp=now() - timedelta(days=1),
            rpg_status=2,  # Cancellation
            room_id=102,
            night_of_stay=self.today - timedelta(days=1),
            id=99999998
        )

    def test_get_events_happy_path(self):
        # Test a successful GET request with limit and offset
        response = self.client.get(self.url, {
            'limit': 10,
            'offset': 0,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return all events

    def test_get_events_with_filters(self):
        # Test GET request with filters applied
        response = self.client.get(self.url, {
            'hotel_id': 1,
            'limit': 10,
            'offset': 0,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

        # Filter by rpg_status
        response = self.client.get(self.url, {
            'rpg_status': 1,  # Booking
            'limit': 10,
            'offset': 0,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_events_with_date_filters(self):
        # Test filtering by timestamp
        response = self.client.get(self.url, {
            'updated_gte': (now() - timedelta(days=2)).isoformat(),
            'updated_lte': now().isoformat(),
            'limit': 10,
            'offset': 0,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_events_invalid_limit_and_offset(self):
        # Test missing limit and offset
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test non-integer limit and offset
        response = self.client.get(self.url, {
            'limit': 'abc',
            'offset': 'xyz'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('limit and offset must be integers', response.data['message'])

    def test_post_event_happy_path(self):
        # Test a successful POST request
        new_event_data = {
            'id': 999928389,
            'hotel_id': 2,
            'timestamp': now().isoformat(),
            'rpg_status': 1,
            'room_id': 201,
            'night_of_stay': self.today.isoformat(),
        }
        response = self.client.post(self.url, new_event_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 3)  # We had 2 events before

    def test_post_event_invalid_data(self):
        # Test POST request with missing fields
        invalid_event_data = {
            'id': 999928388,
            'hotel_id': 2,
            'timestamp': now().isoformat(),
            # Missing rpg_status
            'room_id': 201,
            'night_of_stay': self.today.isoformat(),
        }
        response = self.client.post(self.url, invalid_event_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('rpg_status', response.data)

    def test_get_events_with_limit_and_offset_pagination(self):
        # Test pagination with limit and offset
        response = self.client.get(self.url, {
            'limit': 1,
            'offset': 0,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.get(self.url, {
            'limit': 1,
            'offset': 1,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_events_no_results_with_filters(self):
        # Test filters that result in no matching records
        response = self.client.get(self.url, {
            'hotel_id': 99,  # Non-existent hotel_id
            'limit': 10,
            'offset': 0,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Should return an empty list
