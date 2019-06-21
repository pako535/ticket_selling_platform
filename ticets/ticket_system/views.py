from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters

from ticket_system.services.utils import update_reservation_states
from .models import Event, Reservation
from ticket_system.api.serializers import EventSerializer, ReservationSerializer, PaySerializer
from ticket_system.services.pay import PaymentServices
from ticket_system.services.statistics import StatisticsServices
from ticket_system.services.reservation import ReservationServices
from ticket_system.services.info_available_ticket import InfoAvailableTicketsServices


class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = '__all__'

    def get(self, request, *args, **kwargs):
        update_reservation_states()
        return super().get(request, *args, **kwargs)


class InfoAvailableTicketsView(APIView):

    def get(self, request, *args, **kwargs):
        return Response(InfoAvailableTicketsServices().get_event_info())


"""
    To get info about reservation, you must pass existing id.
"""


class ReservationListView(APIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get(self, request):
        reservation_id = self.request.query_params.get('id', None)
        if reservation_id:
            response = ReservationServices().get_reservation_info(reservation_id)
            return Response(response)
        return Response({'error': 'Pass reservation id'})

    def post(self, request):
        return Response(ReservationServices().create_reservation(request))


class StatisticsView(APIView):

    def get(self, request):
        stat = StatisticsServices()
        stat.generate_statistics()
        response = stat.get_response()
        return Response(response)


class PayForTicket(generics.CreateAPIView):
    serializer_class = PaySerializer

    def post(self, request, *args, **kwargs):
        payment_gateway = PaymentServices()
        payment_gateway.get_reservation(request.data.get('reservation_id'))
        response = payment_gateway.charge(
            request.data.get('amount'),
            request.data.get('token'),
            request.data.get('currency')
        )
        return Response({'result': response})
