from django.db import models

class Event(models.Model):
    BOOKING = 1
    CANCELLATION = 2
    RPG_STATUS_CHOICES = [
        (BOOKING, 'Booking'),
        (CANCELLATION, 'Cancellation'),
    ]
    
    id = models.CharField(max_length=36, primary_key=True, unique=True)
    room_id = models.CharField(max_length=36)
    night_of_stay = models.DateField()
    rpg_status = models.IntegerField(choices=RPG_STATUS_CHOICES)
    timestamp = models.DateTimeField()
    hotel_id = models.CharField(max_length=36)

    def __str__(self):
        return f"Event {self.id} - Hotel {self.hotel_id}"
