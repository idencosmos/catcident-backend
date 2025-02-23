# uploads/views.py
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Media
from .serializers import MediaSerializer


def handle_media_upload(file_obj):
    """공통 미디어 업로드 처리 로직"""
    hash_value = Media.calculate_file_hash(file_obj)
    existing_media = Media.objects.filter(hash_value=hash_value).first()
    if existing_media:
        return existing_media
    media = Media(
        file=file_obj, hash_value=hash_value, title=file_obj.name.split("/")[-1]
    )
    media.save()
    return media


class MediaUploadView(generics.CreateAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        file = self.request.FILES["file"]
        media = handle_media_upload(file)
        if media != serializer.instance:
            serializer.instance = media


class MediaListView(generics.ListAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [IsAdminUser]


class CKEditor5UploadView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get("upload")
        if not file_obj:
            return JsonResponse({"error": "No file uploaded"}, status=400)
        media = handle_media_upload(file_obj)
        return JsonResponse({"url": media.file.url})
