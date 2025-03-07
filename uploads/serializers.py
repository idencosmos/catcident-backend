# uploads/serializers.py
from rest_framework import serializers
from .models import Media


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ["id", "file", "uploaded_at", "title", "is_used_cached"]
