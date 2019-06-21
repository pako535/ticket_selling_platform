import datetime

from ticket_system.models import Reservation, Event
from ticket_system.api.serializers import ReservationSerializer


"""
    Busines logick for reservations.
"""


class ReservationServices:

    def get_reservation_info(self, reservation_id):
        reservation = Reservation.objects.filter(
            id=reservation_id).first()
        if reservation:
            reservation.update_reservation()
            response = [ReservationSerializer(reservation).data]
            response[0]['date_and_time_of_reservation'] = reservation.date_and_time_of_reservation
            response[0]['state'] = reservation.state
        else:
            response = [
                {'error': 'Reservation with the given id does not exist'}]
        return response

    def create_reservation(self, request):
        event = Event.objects.filter(id=request.data.get('event')).first()
        type_ticket = request.data.get('type_ticket')
        if event and type_ticket:
            ticket = self.get_ticket(event, type_ticket)
            reservation = Reservation(
                first_name_client=request.data.get(
                    'first_name_client',
                    'None'),
                last_name_client=request.data.get(
                    'last_name_client',
                    'None'),
                email=request.data.get(
                    'email',
                    'None'),
                phone_number=request.data.get(
                    'phone_number',
                    'None'),
                date_and_time_of_reservation=datetime.datetime.now(),
                event=event,
                type_ticket=type_ticket,
                ticket=ticket)
            reservation.save()
            return [ReservationSerializer(reservation).data]
        return [{'error': 'The given ticket type or reservation is incorrect'}]
    
    @staticmethod
    def get_ticket(event, type_ticket):
        if event.student_ticket.type_ticket == type_ticket:
            ticket = event.student_ticket
        elif event.normal_ticket.type_ticket == type_ticket:
            ticket = event.normal_ticket
        elif event.premium_ticket.type_ticket == type_ticket:
            ticket = event.premium_ticket
        elif event.vip_ticket.type_ticket == type_ticket:
            ticket = event.vip_ticket
        return ticket
