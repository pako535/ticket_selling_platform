from django.conf.urls import url
from ticket_system.views import EventListView, \
    InfoAvailableTicketsView, \
    ReservationListView, \
    StatisticsView, \
    PayForTicket

urlpatterns = [
    url(r'^event/$', EventListView.as_view(), name='event_list'),
    url(r'^available_tickets/$', InfoAvailableTicketsView.as_view(), name='available_tickets'),
    url(r'^reserve/$', ReservationListView.as_view(), name='reserve_ticket'),
    url(r'^statistics/$', StatisticsView.as_view(), name='statistics'),
    url(r'^pay/$', PayForTicket.as_view(), name='pay'),
]
