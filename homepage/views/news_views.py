# homepage/views/news_views.py
from rest_framework import generics
from rest_framework.permissions import AllowAny
from homepage.models.news_models import NewsCategory, News
from homepage.serializers.news_serializers import NewsCategorySerializer, NewsSerializer

class NewsCategoryListAPIView(generics.ListAPIView):
    queryset = NewsCategory.objects.all()
    serializer_class = NewsCategorySerializer
    permission_classes = [AllowAny]

class NewsListAPIView(generics.ListAPIView):
    queryset = News.objects.select_related("category").all()
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]

class NewsDetailAPIView(generics.RetrieveAPIView):
    queryset = News.objects.select_related("category").all()
    serializer_class = NewsSerializer
    lookup_field = "id"
    permission_classes = [AllowAny]