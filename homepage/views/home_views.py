from rest_framework import generics
from rest_framework.permissions import AllowAny
from homepage.models import HomeSection, HeroSlide
from homepage.serializers.home_serializers import (
    HomeSectionSerializer,
    HeroSlideSerializer,
)


class HomeSectionListAPIView(generics.ListAPIView):
    queryset = HomeSection.objects.filter(is_active=True).order_by("order")
    serializer_class = HomeSectionSerializer
    permission_classes = [AllowAny]


class HeroSlideListAPIView(generics.ListAPIView):
    queryset = HeroSlide.objects.filter(is_active=True).order_by("order")
    serializer_class = HeroSlideSerializer
    permission_classes = [AllowAny]
