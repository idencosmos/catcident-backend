# homepage/views/global_views.py
from rest_framework import generics
from rest_framework.permissions import AllowAny

from homepage.models.global_models import (
    SiteTitle,
    NavigationGroup,
    FooterSection,
    FamilySite,
    Copyright
)
from homepage.serializers.global_serializers import (
    SiteTitleSerializer,
    NavigationGroupSerializer,
    FooterSectionSerializer,
    FamilySiteSerializer,
    CopyrightSerializer
)

class SiteTitleDetailAPIView(generics.RetrieveAPIView):
    queryset = SiteTitle.objects.all()
    serializer_class = SiteTitleSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        # 단일 레코드만 있다고 가정
        return self.get_queryset().first()


class NavigationGroupListAPIView(generics.ListAPIView):
    queryset = NavigationGroup.objects.prefetch_related("sub_menus").all()
    serializer_class = NavigationGroupSerializer
    permission_classes = [AllowAny]


class FooterSectionListAPIView(generics.ListAPIView):
    queryset = FooterSection.objects.prefetch_related("sub_menus").all()
    serializer_class = FooterSectionSerializer
    permission_classes = [AllowAny]


class FamilySiteListAPIView(generics.ListAPIView):
    queryset = FamilySite.objects.all()
    serializer_class = FamilySiteSerializer
    permission_classes = [AllowAny]


class CopyrightDetailAPIView(generics.RetrieveAPIView):
    queryset = Copyright.objects.all()
    serializer_class = CopyrightSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return self.get_queryset().first()
