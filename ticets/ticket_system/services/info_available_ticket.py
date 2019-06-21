from django.db.models import Q

from ticket_system.models import States, TypeTickets, Event, Reservation
from ticket_system.services.utils import update_reservation_states


"""
    Busines logick for get available_ticke
"""


class InfoAvailableTicketsServices:

    def get_event_info(self):
        response = []
        update_reservation_states()
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

        return response

    @staticmethod
    def count_available_tickets(type_ticket, total_count_ticets, event):
        return total_count_ticets - len(Reservation.objects.filter(
            (Q(state=States.PAID.name) | Q(state=States.RESERVED.name)),
            ticket__type_ticket=type_ticket.name,
            event=event))
