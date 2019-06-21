import datetime
from django.db.models import Count, Q

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import States, TypeTickets, Event, Reservation
from .api.serializers import EventSerializer, ReservationSerializer


# TODO update rezerwacji dla statystyk i pobierania info

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
        return total_count_ticets - len(Reservation.objects.filter(
            (Q(state=States.CANCELED.name) | Q(state=States.RESERVED.name)),
            ticket__type_ticket=type_ticket.name,
            event=event))


class ReservationListView(APIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    
    def get(self, request):
        reservation_id = self.request.query_params.get('id', None)
        if reservation_id:
            reservation = Reservation.objects.filter(
                id=reservation_id).first()
            reservation._update_reservation()
            response = [ReservationSerializer(reservation).data]
            response[0]['date_and_time_of_reservation'] = reservation.date_and_time_of_reservation
            return Response(response)
        return Response({'message': 'Pass reservation id'})
    
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


class Statistics(APIView):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total_student_ticket = 0
        self.total_normal_ticket = 0
        self.total_premium_ticket = 0
        self.total_vip_ticket = 0
    
    def get(self, request):
        events = Event.objects.all()
        response = []
        
        """
        Get ticket statistics for each event
        """
        for event in events:
            ticket_statistics = self.count_bought_tickets(event)
            response.append(dict(
                event_name=event.name,
                amount_student_ticket=ticket_statistics.get('student', 0),
                amount_normal_ticket=ticket_statistics.get('normal', 0),
                amount_premium_ticket=ticket_statistics.get('premium', 0),
                amount_vip_ticket=ticket_statistics.get('vip', 0),
                total_ticket_sum=ticket_statistics.get('total_sum')
            
            ))
        """
            Get totals different kinds of tickets
        """
        response.append(dict(
            total_student_ticket=self.total_student_ticket,
            total_normal_ticket=self.total_normal_ticket,
            total_premium_ticket=self.total_premium_ticket,
            total_vip_ticket=self.total_vip_ticket
        ))
        
        return Response(response)
    
    def count_bought_tickets(self, event):
        ticket_statistics = Reservation.objects \
            .values('ticket') \
            .filter(event_id=event.id) \
            .annotate(amount=Count('ticket'))
        
        scores = dict()
        total_sum = 0
        for i in ticket_statistics:
            total_sum += i['amount']
            if i['ticket'] == event.student_ticket.id:
                scores['student'] = i['amount']
                self.total_student_ticket += i['amount']
            elif i['ticket'] == event.normal_ticket.id:
                scores['normal'] = i['amount']
                self.total_normal_ticket += i['amount']
            elif i['ticket'] == event.premium_ticket.id:
                scores['premium'] = i['amount']
                self.total_premium_ticket += i['amount']
            elif i['ticket'] == event.vip_ticket.id:
                scores['vip'] = i['amount']
                self.total_vip_ticket += i['amount']
        scores['total_sum'] = total_sum
        return scores
