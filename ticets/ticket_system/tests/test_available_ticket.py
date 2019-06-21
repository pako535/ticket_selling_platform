from ticket_system.models import States
from ticket_system.tests.base import BaseTest


class AvailableTicketsTest(BaseTest):

    @classmethod
    def setUpClass(cls):
        super(AvailableTicketsTest, cls).setUpClass()
        cls.AVAILABLE_TICKET_URL = '/available_tickets/'

    def test_amount_available_ticket(self):
        response = self.client.get(self.AVAILABLE_TICKET_URL)
        self.assertContains(
            response, '\"available_student_tickets\":{}'.format(
                self.event.total_student_tickets - 1))

    def test_amount_available_ticket_with_canceled_reservatio(self):
        self.reservation.state = States.CANCELED.name
        self.reservation.save()

        response = self.client.get(self.AVAILABLE_TICKET_URL)
        self.assertContains(
            response, '\"available_student_tickets\":{}'.format(
                self.event.total_student_tickets))
