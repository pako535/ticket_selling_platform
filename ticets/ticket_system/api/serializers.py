from rest_framework import serializers
from ticket_system.models import Event, Reservation


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = (
            'student_ticket',
            'normal_ticket',
            'premium_ticket',
            'vip_ticket')


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        exclude = ('date_and_time_of_reservation', 'ticket', 'state')


class PaySerializer(serializers.Serializer):
    amount = serializers.FloatField()
    token = serializers.CharField()
    currency = serializers.CharField()
    reservation_id = serializers.IntegerField()
