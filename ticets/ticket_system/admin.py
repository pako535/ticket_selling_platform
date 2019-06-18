from django.contrib import admin
from ticket_system.models import Event, Ticket, Reservation

# Register your models here.

admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(Reservation)
