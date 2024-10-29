from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Event
from .serializers import EventSerializer
from django.utils.dateparse import parse_datetime, parse_date


class EventViewSet(APIView):
    def get(self, request):
        # Get query parameters
        hotel_id = request.query_params.get('hotel_id')
        timestamp_gte = request.query_params.get('updated_gte')
        timestamp_lte = request.query_params.get('updated_lte')
        rpg_status = request.query_params.get('rpg_status')
        room_id = request.query_params.get('room_id')
        night_of_stay_gte = request.query_params.get('night_of_stay_gte')
        night_of_stay_lte = request.query_params.get('night_of_stay_lte')
        limit = request.query_params.get('limit')
        offset = request.query_params.get('offset')

        # Validate limit and offset parameters
        if not limit or not offset:
            return Response({'message': 'limit and offset params are required'}, status=400)

        try:
            limit = int(limit)
            offset = int(offset)
        except ValueError:
            return Response({'message': 'limit and offset must be integers'}, status=400)

        # Start with all events and apply ordering
        events = Event.objects.all().order_by('timestamp')

        # Apply filters based on query parameters
        if hotel_id:
            events = events.filter(hotel_id=hotel_id)
        if timestamp_gte:
            parsed_gte = parse_datetime(timestamp_gte)
            if parsed_gte:
                events = events.filter(timestamp__gte=parsed_gte)
        if timestamp_lte:
            parsed_lte = parse_datetime(timestamp_lte)
            if parsed_lte:
                events = events.filter(timestamp__lte=parsed_lte)
        if rpg_status:
            events = events.filter(rpg_status=rpg_status)
        if room_id:
            events = events.filter(room_id=room_id)
        if night_of_stay_gte:
            parsed_night_of_stay_gte = parse_date(night_of_stay_gte)
            if parsed_night_of_stay_gte:
                events = events.filter(night_of_stay__gte=parsed_night_of_stay_gte)
        if night_of_stay_lte:
            parsed_night_of_stay_lte = parse_date(night_of_stay_lte)
            if parsed_night_of_stay_lte:
                events = events.filter(night_of_stay__lte=parsed_night_of_stay_lte)

        # Apply limit and offset after all filters
        events = events[offset:offset + limit]

        # Serialize the filtered events
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


    def post(self, request):
        # Deserialize the data to create a new event
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)