# homepage/views/about_views.py

from rest_framework import generics
from rest_framework.permissions import AllowAny

from homepage.models.about_models import (
    Creator, BookCategory, Book,
    Character, HistoryEvent, LicensePage
)
from homepage.serializers.about_serializers import (
    CreatorSerializer, BookCategorySerializer,
    BookSerializer, CharacterSerializer,
    HistoryEventSerializer, LicensePageSerializer
)

# 1) Creator
class CreatorListAPIView(generics.ListAPIView):
    queryset = Creator.objects.all()
    serializer_class = CreatorSerializer
    permission_classes = [AllowAny]


class CreatorDetailAPIView(generics.RetrieveAPIView):
    queryset = Creator.objects.all()
    serializer_class = CreatorSerializer
    lookup_field = "slug"
    permission_classes = [AllowAny]


# 2) BookCategory
class BookCategoryListAPIView(generics.ListAPIView):
    queryset = BookCategory.objects.all()
    serializer_class = BookCategorySerializer
    permission_classes = [AllowAny]


# 3) Book
class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.select_related("category").prefetch_related("authors")
    serializer_class = BookSerializer
    permission_classes = [AllowAny]


class BookDetailAPIView(generics.RetrieveAPIView):
    queryset = Book.objects.select_related("category").prefetch_related("authors")
    serializer_class = BookSerializer
    lookup_field = "pk"
    permission_classes = [AllowAny]


# 4) Character
class CharacterListAPIView(generics.ListAPIView):
    queryset = Character.objects.prefetch_related("books", "creator")
    serializer_class = CharacterSerializer
    permission_classes = [AllowAny]


class CharacterDetailAPIView(generics.RetrieveAPIView):
    queryset = Character.objects.prefetch_related("books", "creator")
    serializer_class = CharacterSerializer
    lookup_field = "slug"
    permission_classes = [AllowAny]


# 5) History
class HistoryEventListAPIView(generics.ListAPIView):
    queryset = HistoryEvent.objects.all()
    serializer_class = HistoryEventSerializer
    permission_classes = [AllowAny]


# 6) LicensePage
class LicensePageDetailAPIView(generics.RetrieveAPIView):
    queryset = LicensePage.objects.all()
    serializer_class = LicensePageSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        # 단일 레코드만 존재한다고 가정하고 첫 번째 객체 반환
        return self.queryset.first()
