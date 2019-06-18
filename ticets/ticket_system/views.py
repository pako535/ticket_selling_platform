import datetime
from django.http import HttpResponseRedirect

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import Ticket, TypeTickets, Event, Reservation
from .api.serializers import EventSerializer, ReservationSerializer


class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class InfoEventView(APIView):
    
    def get(self, request):
        response = []
        for event in Event.objects.all():
            response.append(dict(
                name=event.name,
                available_student_tickets=self.count_available_tickets(
                    TypeTickets.STUDENT,
                    event.total_student_tickets,
                    event
                ),
                available_normal_tickets=self.count_available_tickets(
                    TypeTickets.NORMAL,
                    event.total_normal_tickets,
                    event
                ),
                available_premium_tickets=self.count_available_tickets(
                    TypeTickets.PREMIUM,
                    event.total_premium_tickets,
                    event
                ),
                available_vip_tickets=self.count_available_tickets(
                    TypeTickets.VIP,
                    event.total_vip_tickets,
                    event
                ),
                student_ticket_price=event.student_ticket.price,
                normal_ticket_price=event.normal_ticket.price,
                premium_ticket_price=event.premium_ticket.price,
                vip_ticket_price=event.vip_ticket.price,
            ))
        return Response(response)
    
    @staticmethod
    def count_available_tickets(type_ticket, total_count_ticets, event):
        return total_count_ticets - len(Reservation.objects.filter(ticket__type_ticket=type_ticket.name,
                                                                   event=event))


class ReservationListView(generics.ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    
    def get_queryset(self):

        return None
    
    def post(self, request):
        event = Event.objects.filter(id=request.data.get('event')).first()
        type_ticket = request.data.get('type_ticket')
        if event.student_ticket.type_ticket == type_ticket:
            ticket = event.student_ticket
        elif event.normal_ticket.type_ticket == type_ticket:
            ticket = event.normal_ticket
        elif event.premium_ticket.type_ticket == type_ticket:
            ticket = event.premium_ticket
        elif event.vip_ticket.type_ticket == type_ticket:
            ticket = event.vip_ticket
        reservation = Reservation(
                first_name_client=request.data.get('first_name_client', 'None'),
                last_name_client=request.data.get('last_name_client', 'None'),
                email=request.data.get('email', 'None'),
                phone_number=request.data.get('phone_number', 'None'),
                date_and_time_of_reservation=datetime.datetime.now(),
                event=event,
                type_ticket=type_ticket,
                ticket=ticket
            )
        reservation.save()
        return Response([ReservationSerializer(reservation).data])
