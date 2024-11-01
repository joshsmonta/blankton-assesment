from drf_yasg import openapi

hotel_id_param = openapi.Parameter(
    'hotel_id', 
    openapi.IN_QUERY, 
    description="ID of the hotel", 
    type=openapi.TYPE_INTEGER
)

timestamp_gte_param = openapi.Parameter(
    'timestamp_gte', 
    openapi.IN_QUERY, 
    description="Timestamp greater than or equal to (start of date range)", 
    type=openapi.TYPE_STRING, 
    format=openapi.FORMAT_DATETIME
)

timestamp_lte_param = openapi.Parameter(
    'timestamp_lte', 
    openapi.IN_QUERY, 
    description="Timestamp less than or equal to (end of date range)", 
    type=openapi.TYPE_STRING, 
    format=openapi.FORMAT_DATETIME
)

rpg_status_param = openapi.Parameter(
    'rpg_status', 
    openapi.IN_QUERY, 
    description="RPG status filter", 
    type=openapi.TYPE_STRING
)

room_id_param = openapi.Parameter(
    'room_id', 
    openapi.IN_QUERY, 
    description="ID of the room", 
    type=openapi.TYPE_INTEGER
)

night_of_stay_gte_param = openapi.Parameter(
    'night_of_stay_gte', 
    openapi.IN_QUERY, 
    description="Minimum night of stay (start date of stay range)", 
    type=openapi.TYPE_STRING, 
    format=openapi.FORMAT_DATE
)

night_of_stay_lte_param = openapi.Parameter(
    'night_of_stay_lte', 
    openapi.IN_QUERY, 
    description="Maximum night of stay (end date of stay range)", 
    type=openapi.TYPE_STRING, 
    format=openapi.FORMAT_DATE
)

limit_param = openapi.Parameter(
    'limit', 
    openapi.IN_QUERY, 
    description="Number of results to return per page", 
    type=openapi.TYPE_INTEGER
)

offset_param = openapi.Parameter(
    'offset', 
    openapi.IN_QUERY, 
    description="Starting point of results (used for pagination)", 
    type=openapi.TYPE_INTEGER
)
