# homepage/views/events_views.py
from rest_framework import generics
from rest_framework.permissions import AllowAny
from homepage.models.events_models import EventCategory, Event
from homepage.serializers.events_serializers import EventCategorySerializer, EventSerializer

class EventCategoryListAPIView(generics.ListAPIView):
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    permission_classes = [AllowAny]

class EventListAPIView(generics.ListAPIView):
    queryset = Event.objects.select_related("category").all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]

class EventDetailAPIView(generics.RetrieveAPIView):
    queryset = Event.objects.select_related("category").all()
    serializer_class = EventSerializer
    lookup_field = "id"
    permission_classes = [AllowAny]