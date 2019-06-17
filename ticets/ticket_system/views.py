from rest_framework import generics

from .models import Ticet, TypeTicets, Event
from .api.serializers import EventSerializer


class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
