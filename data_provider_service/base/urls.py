from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import EventViewSet
schema_view = get_schema_view(
   openapi.Info(
      title="Data Provider Service API",
      default_version="v1",
      description="Contains documentation on Data Provider Service APIs",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
)
urlpatterns = [
    path('events/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('events/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('events/', EventViewSet.as_view(), name='event-list-create'),
]