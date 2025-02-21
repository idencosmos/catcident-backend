# homepage/serializers/events_serializers.py
from rest_framework import serializers
from homepage.models.events_models import EventCategory, Event
from uploads.serializers import MediaSerializer

class EventCategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = EventCategory
        fields = ["id", "slug", "name"]

    def get_name(self, obj):
        return obj.safe_translation_getter("name", any_language=True)

class EventSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    category = EventCategorySerializer(read_only=True)
    main_image = MediaSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ["id", "title", "description", "category", "main_image", "date", "created_at"]

    def get_title(self, obj):
        return obj.safe_translation_getter("title", any_language=True)

    def get_description(self, obj):
        return obj.safe_translation_getter("description", any_language=True)