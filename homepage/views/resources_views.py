# homepage/views/resources_views.py
from rest_framework import generics
from rest_framework.permissions import AllowAny
from homepage.models.resources_models import ResourceCategory, Resource
from homepage.serializers.resources_serializers import ResourceCategorySerializer, ResourceSerializer

class ResourceCategoryListAPIView(generics.ListAPIView):
    queryset = ResourceCategory.objects.all()
    serializer_class = ResourceCategorySerializer
    permission_classes = [AllowAny]

class ResourceListAPIView(generics.ListAPIView):
    queryset = Resource.objects.select_related("category").all()
    serializer_class = ResourceSerializer
    permission_classes = [AllowAny]

class ResourceDetailAPIView(generics.RetrieveAPIView):
    queryset = Resource.objects.select_related("category").all()
    serializer_class = ResourceSerializer
    lookup_field = "id"
    permission_classes = [AllowAny]