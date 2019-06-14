from django.db import models
from enum import Enum


# Create your models here.

class TypeTicets(Enum):
    STUDENT = 1
    NORMAL = 2
    PREMIUM = 3
    VIP = 4


class Ticet(models.Model):
    price = models.FloatField(verbose_name='Price')
    ticet_type = models.CharField(max_length=1, choices=TypeTicets)
    date_and_time_of_reservation = models.DateField(verbose_name='Date and time of reservation')


class Event(models.Model):
    name = models.CharField(max_length=120, verbose_name='Name of event')
    start_date_and_time = models.DateField(verbose_name='Start date and time')
    end_date_and_time = models.DateField(verbose_name='End date and time')
    available_student_ticets = models.IntegerField(verbose_name="Available student ticets")
    available_normal_ticets = models.IntegerField(verbose_name="Available normal ticets")
    available_premium_ticets = models.IntegerField(verbose_name="Available premium ticets")
    available_vip_ticets = models.IntegerField(verbose_name="Available vip ticets")


class Reservation(models.Model):
    pass
