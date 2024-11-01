from drf_yasg import openapi
hotel_id_param = openapi.Parameter(
    'hotel_id', 
    openapi.IN_QUERY, 
    description="ID of the hotel", 
    type=openapi.TYPE_INTEGER
)

period_param = openapi.Parameter(
    'period', 
    openapi.IN_QUERY, 
    description="Time period (day, month, year)", 
    type=openapi.TYPE_STRING
)

year_param = openapi.Parameter(
    'year', 
    openapi.IN_QUERY, 
    description="Year for the report (e.g., 2023)", 
    type=openapi.TYPE_INTEGER
)

updated_gte_param = openapi.Parameter(
    'updated_gte', 
    openapi.IN_QUERY, 
    description="get all data from this timestamp param", 
    type=openapi.TYPE_INTEGER
)