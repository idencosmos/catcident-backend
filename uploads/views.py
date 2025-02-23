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
        file = self.request.FILES['file']
        hash_value = Media._calculate_file_hash(file)
        existing_media = Media.objects.filter(hash_value=hash_value).first()
        if existing_media:
            serializer.instance = existing_media  # 중복 시 기존 객체 반환
        else:
            serializer.save(hash_value=hash_value)


class MediaListView(generics.ListAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [IsAdminUser]