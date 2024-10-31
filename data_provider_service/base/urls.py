from django.urls import path
from .views import EventViewSet

urlpatterns = [
    path('events/', EventViewSet.as_view(), name='event-list-create'),
]