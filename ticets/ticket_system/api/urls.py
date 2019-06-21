from django.conf.urls import url
from ticket_system.views import EventListView, \
    InfoEventView, \
    ReservationListView, \
    Statistics

urlpatterns = [
    url(r'^event/$', EventListView.as_view(), name='event_list'),
    url(r'^info_event/$', InfoEventView.as_view(), name='info_event'),
    url(r'^reserve/$', ReservationListView.as_view(), name='reserve_ticket'),
    url(r'^statistics/$', Statistics.as_view(), name='statistics'),
]
