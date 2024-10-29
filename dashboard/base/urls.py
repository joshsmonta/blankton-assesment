from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import DashboardView

schema_view = get_schema_view(
   openapi.Info(
      title="Dashboard Service API",
      default_version="v1",
      description="Contains documentation on dashboard service APIs",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
)
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard-view'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]