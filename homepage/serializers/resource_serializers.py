# homepage/serializers/resource_serializers.py
from rest_framework import serializers
from homepage.models.resource_models import ResourceCategory, Resource
from uploads.serializers import MediaSerializer

class ResourceCategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = ResourceCategory
        fields = ["id", "slug", "name"]

    def get_name(self, obj):
        return obj.safe_translation_getter("name", any_language=True)

class ResourceSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    category = ResourceCategorySerializer(read_only=True)
    main_image = MediaSerializer(read_only=True)
    file = MediaSerializer(read_only=True)

    class Meta:
        model = Resource
        fields = ["id", "title", "description", "category", "main_image", "file", "created_at"]

    def get_title(self, obj):
        return obj.safe_translation_getter("title", any_language=True)

    def get_description(self, obj):
        return obj.safe_translation_getter("description", any_language=True)