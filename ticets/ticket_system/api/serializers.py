from rest_framework import serializers
from ticket_system.models import Event, Reservation, Ticket


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        exclude = ('date_and_time_of_reservation', 'ticket')
