from django.conf.urls import url
from ticket_system.views import EventListView

urlpatterns = [
    url(r'^event/$', EventListView.as_view(), name='event_list'),
]
