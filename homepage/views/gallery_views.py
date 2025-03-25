# homepage/views/gallery_views.py
# 갤러리 콘텐츠에 대한 API 뷰를 정의합니다.

from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.db.models import Prefetch

from homepage.models.gallery_models import GalleryCategory, GalleryItem
from homepage.serializers.gallery_serializers import (
    GalleryCategorySerializer,
    GalleryItemListSerializer,
    GalleryItemDetailSerializer,
)


class GalleryCategoryListAPIView(generics.ListAPIView):
    """갤러리 카테고리 목록 API"""

    queryset = GalleryCategory.objects.all()
    serializer_class = GalleryCategorySerializer
    permission_classes = [AllowAny]


class GalleryItemListAPIView(generics.ListAPIView):
    """갤러리 아이템 목록 API"""

    queryset = GalleryItem.objects.select_related("category", "image").all()
    serializer_class = GalleryItemListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()

        # 카테고리 필터링
        category_slug = self.request.query_params.get("category")
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # 특정 연도 필터링
        year = self.request.query_params.get("year")
        if year:
            queryset = queryset.filter(year=year)

        # 메인 표시 아이템 필터링
        featured = self.request.query_params.get("featured")
        if featured and featured.lower() == "true":
            queryset = queryset.filter(is_featured=True)

        return queryset


class GalleryItemDetailAPIView(generics.RetrieveAPIView):
    """갤러리 아이템 상세 API"""

    queryset = GalleryItem.objects.select_related("category", "image")
    serializer_class = GalleryItemDetailSerializer
    lookup_field = "id"
    permission_classes = [AllowAny]
