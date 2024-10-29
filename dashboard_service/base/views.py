from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from datetime import datetime

class DashboardView(APIView):
    def get(self, request):
        # Get query parameters
        hotel_id = request.query_params.get('hotel_id')
        period = request.query_params.get('period')
        year = request.query_params.get('year')

        # Validate parameters
        if not hotel_id or not period or not year:
            return Response({'message': 'hotel_id, period, and year parameters are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            hotel_id = int(hotel_id)
            year = int(year)
        except ValueError:
            return Response({'message': 'hotel_id and year must be integers'}, status=status.HTTP_400_BAD_REQUEST)

        # Define response data
        data = []

        # SQL query based on the requested period
        if period == 'day':
            query = """
                SELECT 
                    hotel_id,
                    night_of_stay AS day,
                    COUNT(CASE WHEN rpg_status = 1 THEN 1 END) AS daily_bookings,
                    COUNT(CASE WHEN rpg_status = 2 THEN 1 END) AS daily_cancellations,
                    COUNT(DISTINCT room_id) AS rooms_occupied, 
                    COUNT(DISTINCT room_id) * 100.0 / (SELECT COUNT(*) FROM base_dashboardevent WHERE hotel_id = b.hotel_id) AS occupancy_rate
                FROM
                    base_dashboardevent b
                WHERE hotel_id = 2607
                GROUP BY 
                    hotel_id, night_of_stay
                ORDER BY 
                    night_of_stay;
            """
            params = [hotel_id, hotel_id, str(year)]

        elif period == 'month':
            query = """
                SELECT 
                    DATE_TRUNC('month', night_of_stay) AS month,
                    COUNT(CASE WHEN rpg_status = 1 THEN 1 END) AS monthly_bookings,
                    COUNT(CASE WHEN rpg_status = 2 THEN 1 END) AS monthly_cancellations,
                    COUNT(DISTINCT room_id) AS unique_rooms_occupied,
                    COUNT(DISTINCT room_id) * 100.0 / (SELECT COUNT(DISTINCT room_id) FROM base_dashboardevent WHERE hotel_id = %s) AS occupancy_rate
                FROM 
                    base_dashboardevent
                WHERE
                    hotel_id = %s AND strftime('%Y', night_of_stay) = %s
                GROUP BY 
                    hotel_id, month
                ORDER BY 
                    month;
            """
            params = [hotel_id, hotel_id, str(year)]

        elif period == 'year':
            query = """
                SELECT 
                    DATE_TRUNC('year', night_of_stay) AS year,
                    COUNT(CASE WHEN rpg_status = 1 THEN 1 END) AS yearly_bookings,
                    COUNT(CASE WHEN rpg_status = 2 THEN 1 END) AS yearly_cancellations,
                    COUNT(DISTINCT room_id) AS unique_rooms_occupied,
                    COUNT(DISTINCT room_id) * 100.0 / (SELECT COUNT(DISTINCT room_id) FROM base_dashboardevent WHERE hotel_id = %s) AS occupancy_rate
                FROM 
                    base_dashboardevent
                WHERE
                    hotel_id = %s AND strftime('%Y', night_of_stay) = %s
                GROUP BY 
                    hotel_id, year
                ORDER BY 
                    year;
            """
            params = [hotel_id, hotel_id, str(year)]

        else:
            return Response({'message': 'Invalid period. Must be "day", "month", or "year".'}, status=status.HTTP_400_BAD_REQUEST)

        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            data = [dict(zip(columns, row)) for row in rows]

        return Response(data, status=status.HTTP_200_OK)
