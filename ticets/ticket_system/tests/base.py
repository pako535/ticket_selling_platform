import datetime
from django.test import TestCase
from ticket_system.models import Event, Ticket, TypeTickets, Reservation


class BaseTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(BaseTest, cls).setUpClass()
        cls.event = Event(
            name="Event",
            start_date_and_time=datetime.datetime.now(),
            end_date_and_time=datetime.datetime.now() +
            datetime.timedelta(
                hours=2),
            total_student_tickets=4,
            total_normal_tickets=4,
            total_premium_tickets=4,
            total_vip_tickets=4,
            student_ticket=Ticket.objects.create(
                price=20,
                type_ticket=TypeTickets.STUDENT.name),
            normal_ticket=Ticket.objects.create(
                price=20,
                type_ticket=TypeTickets.NORMAL.name),
            premium_ticket=Ticket.objects.create(
                price=20,
                type_ticket=TypeTickets.PREMIUM.name),
            vip_ticket=Ticket.objects.create(
                price=20,
                type_ticket=TypeTickets.VIP.name),
        )
        cls.event.save()

        cls.reservation = Reservation(
            first_name_client="Name",
            last_name_client="Surname",
            email="test@test.com",
            phone_number="123456789",
            event=cls.event,
            ticket=cls.event.student_ticket,
            date_and_time_of_reservation=datetime.datetime.now()
        )
        cls.reservation.save()
