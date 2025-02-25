# homepage/urls.py
from django.urls import path
from homepage.views.global_views import (
    SiteTitleDetailAPIView, NavigationGroupListAPIView,
    FooterSectionListAPIView, FamilySiteListAPIView, CopyrightDetailAPIView
)
from homepage.views.home_views import HomeSectionListAPIView, HeroSlideListAPIView

from homepage.views.about_views import (
    CreatorListAPIView, CreatorDetailAPIView,
    BookCategoryListAPIView, BookListAPIView, BookDetailAPIView,
    CharacterListAPIView, CharacterDetailAPIView,
    HistoryEventListAPIView, LicensePageDetailAPIView
)
from homepage.views.resources_views import (
    ResourceCategoryListAPIView, ResourceListAPIView, ResourceDetailAPIView
)
from homepage.views.news_views import (
    NewsCategoryListAPIView, NewsListAPIView, NewsDetailAPIView
)
from homepage.views.events_views import (
    EventCategoryListAPIView, EventListAPIView, EventDetailAPIView
)

urlpatterns = [
    # Global
    path('global/sitetitle/', SiteTitleDetailAPIView.as_view(), name='sitetitle-detail'),
    path('global/navigation/', NavigationGroupListAPIView.as_view(), name='navigation-list'),
    path('global/footer-sections/', FooterSectionListAPIView.as_view(), name='footer-sections-list'),
    path('global/family-sites/', FamilySiteListAPIView.as_view(), name='family-sites-list'),
    path('global/copyright/', CopyrightDetailAPIView.as_view(), name='copyright-detail'),

    # Home
    path('home/sections/', HomeSectionListAPIView.as_view(), name='home-sections'),
    path('home/hero/', HeroSlideListAPIView.as_view(), name='home-hero'),    

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

    # Resources
    path('resources/categories/', ResourceCategoryListAPIView.as_view(), name='resource-category-list'),
    path('resources/', ResourceListAPIView.as_view(), name='resource-list'),
    path('resources/<int:id>/', ResourceDetailAPIView.as_view(), name='resource-detail'),

    # News
    path('news/categories/', NewsCategoryListAPIView.as_view(), name='news-category-list'),
    path('news/', NewsListAPIView.as_view(), name='news-list'),
    path('news/<int:id>/', NewsDetailAPIView.as_view(), name='news-detail'),

    # Events
    path('events/categories/', EventCategoryListAPIView.as_view(), name='event-category-list'),
    path('events/', EventListAPIView.as_view(), name='event-list'),
    path('events/<int:id>/', EventDetailAPIView.as_view(), name='event-detail'),
]