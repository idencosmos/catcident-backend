# uploads/views.py
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import Media
from .serializers import MediaSerializer


class MediaUploadView(generics.CreateAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save()


class MediaListView(generics.ListAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [IsAdminUser]