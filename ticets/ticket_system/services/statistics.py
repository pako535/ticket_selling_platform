from django.db.models import Count

from ticket_system.models import Event, Reservation, States
from ticket_system.services.utils import update_reservation_states

"""
    Busines logick for get statistics.
    Only paid tickets are counted!!!
"""


class StatisticsServices:
    update_reservation_states()

    def __init__(self):
        self.total_student_ticket = 0
        self.total_normal_ticket = 0
        self.total_premium_ticket = 0
        self.total_vip_ticket = 0
        self.response = []

    def generate_statistics(self):
        self.get_statistic_for_each_event()
        self.get_statistic_for_different_ticket()

    """
         Get ticket statistics for each event
    """

    def get_statistic_for_each_event(self):
        events = Event.objects.all()

        for event in events:
            ticket_statistics = self.count_bought_tickets(event)
            self.response.append(dict(
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

    def get_statistic_for_different_ticket(self):
        self.response.append(dict(
            total_student_ticket=self.total_student_ticket,
            total_normal_ticket=self.total_normal_ticket,
            total_premium_ticket=self.total_premium_ticket,
            total_vip_ticket=self.total_vip_ticket
        ))

    def get_response(self):
        return self.response

    def count_bought_tickets(self, event):
        ticket_statistics = Reservation.objects \
            .values('ticket') \
            .filter(event_id=event.id, state=States.PAID.name) \
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
