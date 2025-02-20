# homepage/urls.py
from django.urls import path
from homepage.views.global_views import (
    SiteTitleDetailAPIView,
    NavigationGroupListAPIView,
    FooterSectionListAPIView,
    FamilySiteListAPIView,
    CopyrightDetailAPIView
)
from homepage.views.about_views import (
    CreatorListAPIView, CreatorDetailAPIView,
    BookCategoryListAPIView, BookListAPIView, BookDetailAPIView,
    CharacterListAPIView, CharacterDetailAPIView,
    HistoryEventListAPIView, LicensePageDetailAPIView
)

urlpatterns = [
    # Global
    path('global/sitetitle/', SiteTitleDetailAPIView.as_view(), name='sitetitle-detail'),
    path('global/navigation/', NavigationGroupListAPIView.as_view(), name='navigation-list'),
    path('global/footer-sections/', FooterSectionListAPIView.as_view(), name='footer-sections-list'),
    path('global/family-sites/', FamilySiteListAPIView.as_view(), name='family-sites-list'),
    path('global/copyright/', CopyrightDetailAPIView.as_view(), name='copyright-detail'),

    # About
    path('about/creators/', CreatorListAPIView.as_view(), name='creator-list'),
    path('about/creators/<slug:slug>/', CreatorDetailAPIView.as_view(), name='creator-detail'),
    path('about/book-categories/', BookCategoryListAPIView.as_view(), name='bookcategory-list'),
    path('about/books/', BookListAPIView.as_view(), name='book-list'),
    path('about/books/<int:pk>/', BookDetailAPIView.as_view(), name='book-detail'),
    path('about/characters/', CharacterListAPIView.as_view(), name='character-list'),
    path('about/characters/<slug:slug>/', CharacterDetailAPIView.as_view(), name='character-detail'),
    path('about/history/', HistoryEventListAPIView.as_view(), name='historyevent-list'),
    path('about/license/', LicensePageDetailAPIView.as_view(), name='licensepage-detail'),
]
