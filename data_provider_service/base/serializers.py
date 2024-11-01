from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        
    def validate(self, data):
        # Example validation: ensure that night_of_stay is not in the past
        if data['night_of_stay'] < data['timestamp'].date():
            raise serializers.ValidationError("The night of stay cannot be in the past.")
        return data
    
    
class EventFields(serializers.BaseSerializer):
    id = serializers.CharField()
    room_id = serializers.CharField()
    night_of_stay = serializers.DateField()
    rpg_status = serializers.IntegerField()
    timestamp = serializers.DateTimeField()
    hotel_id = serializers.CharField()