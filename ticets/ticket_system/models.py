import datetime
from django.db import models
from enum import Enum


# Create your models here.

class TypeTickets(Enum):
    STUDENT = 'STUDENT'
    NORMAL = 'NORMAL'
    PREMIUM = 'PREMIUM'
    VIP = 'VIP'


class States(Enum):
    RESERVED = 'RESERVED'
    PAID = 'PAID'
    CANCELED = 'CANCELED'


class Ticket(models.Model):
    price = models.FloatField(verbose_name='Price')
    type_ticket = models.CharField(
        max_length=7, choices=(
            (x.name, x.name) for x in TypeTickets))

    def __str__(self):
        return str(self.type_ticket) + " | " + str(self.price)


class Event(models.Model):
    name = models.CharField(max_length=120, verbose_name='Name of event')
    start_date_and_time = models.DateTimeField(
        verbose_name='Start date and time')
    end_date_and_time = models.DateTimeField(verbose_name='End date and time')
    total_student_tickets = models.IntegerField(
        verbose_name="Available student tickets")
    total_normal_tickets = models.IntegerField(
        verbose_name="Available normal tickets")
    total_premium_tickets = models.IntegerField(
        verbose_name="Available premium tickets")
    total_vip_tickets = models.IntegerField(
        verbose_name="Available vip tickets")
    student_ticket = models.ForeignKey(
        Ticket,
        on_delete=models.DO_NOTHING,
        related_name='student_ticket',
        verbose_name='Student ticket')
    normal_ticket = models.ForeignKey(
        Ticket,
        on_delete=models.DO_NOTHING,
        related_name='normal_ticket',
        verbose_name='Normal ticket')
    premium_ticket = models.ForeignKey(
        Ticket,
        on_delete=models.DO_NOTHING,
        related_name='premium_ticket',
        verbose_name='Premium ticket')
    vip_ticket = models.ForeignKey(
        Ticket,
        on_delete=models.DO_NOTHING,
        related_name='vip_ticket',
        verbose_name='Vip icket')

    def __str__(self):
        return str(self.name) + " | " + str(self.start_date_and_time)


class Reservation(models.Model):
    first_name_client = models.CharField(
        max_length=120, verbose_name='First name')
    last_name_client = models.CharField(
        max_length=120, verbose_name='Last Name')
    email = models.EmailField(max_length=45, verbose_name='Email')
    phone_number = models.CharField(max_length=11, verbose_name='Phone number')

    date_and_time_of_reservation = models.DateTimeField(
        verbose_name='Date and time of reservation')

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='event',
        verbose_name='Event')

    type_ticket = models.CharField(
        max_length=7, choices=(
            (x.name, x.name) for x in TypeTickets))
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.DO_NOTHING,
        related_name='ticket',
        verbose_name='ticketit')

    state = models.CharField(max_length=8, default=States.RESERVED.name,
                             choices=((x.name, x.name) for x in States))

    def __str__(self):
        return "{} {} | {} | {}".format(
            self.first_name_client,
            self.last_name_client,
            self.ticket,
            self.event
        )

    def update_reservation(self):
        time_difference = (datetime.datetime.now() - self.date_and_time_of_reservation
                           .replace(tzinfo=None)) \
            .total_seconds() / 60.0
        if time_difference >= 15 and self.state == States.RESERVED.value:
            self.state = States.CANCELED.name
            self.save()
