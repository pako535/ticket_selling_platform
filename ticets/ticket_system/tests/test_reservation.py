from ticket_system.tests.base import BaseTest
from ticket_system.models import Reservation


class ReservationTest(BaseTest):

    @classmethod
    def setUpClass(cls):
        super(ReservationTest, cls).setUpClass()
        cls.RESERVE_URL = '/reserve/'

    def test_get_reservation(self):
        response = self.client.get(self.RESERVE_URL)
        self.assertContains(response, 'Pass reservation id')

    def test_get_specified_reservation(self):
        response = self.client.get(self.RESERVE_URL + '?id=1')
        self.assertContains(response, self.reservation.first_name_client)

    def test_get_wrong_specified_reservation(self):
        response = self.client.get(self.RESERVE_URL + '?id=2')
        self.assertContains(
            response, 'Reservation with the given id does not exist')

    def test_post_reservation(self):
        data = {
            'first_name_client': 'Name',
            'last_name_client': 'Surname',
            'email': 'a@test.com',
            'phone_number': '1234567489',
            'event': self.event.id,
            'type_ticket': self.event.vip_ticket.type_ticket
        }
        response = self.client.post(self.RESERVE_URL, data)
        self.assertContains(response, 'last_name_client')
        self.assertEqual(len(Reservation.objects.all()), 2)

    def test_post_reservation_with_wrong_data(self):
        data = {
            'first_name_client': 'Name',
            'last_name_client': 'Surname',
            'email': 'a@test.com',
            'phone_number': '1234567489',
            'event': self.event.id + 10,
            'type_ticket': self.event.vip_ticket.type_ticket
        }
        response = self.client.post(self.RESERVE_URL, data)
        self.assertContains(
            response,
            'The given ticket type or reservation is incorrect')
        self.assertEqual(len(Reservation.objects.all()), 1)
