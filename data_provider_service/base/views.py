from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Event
from .serializers import EventSerializer, EventFields
from django.utils.dateparse import parse_datetime, parse_date
from .swagger import *


class EventViewSet(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            hotel_id_param, 
            timestamp_gte_param, 
            timestamp_lte_param, 
            rpg_status_param, 
            room_id_param, 
            night_of_stay_gte_param, 
            night_of_stay_lte_param, 
            limit_param, 
            offset_param
        ],
        operation_description="Get events using this endpoint.",
        responses={200: EventSerializer}
    )
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
        # Validate limit and offset parameters
        if limit and offset:
            try:
                limit = int(limit)
                offset = int(offset)
            except ValueError:
                return Response({'message': 'limit and offset must be integers'}, status=400)
            events = events[offset:offset + limit]

            # Serialize the filtered events
            serializer = EventSerializer(events, many=True)
            return Response(serializer.data)
        else:
            # Serialize the filtered events
            serializer = EventSerializer(events, many=True)
            return Response(serializer.data)
            

    @swagger_auto_schema(
        request_body=EventSerializer,
        operation_description="Create Events using this endpoint.",
        responses={201: EventSerializer}
    )
    def post(self, request):
        # Deserialize the data to create a new event
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)