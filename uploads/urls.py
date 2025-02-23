# uploads/urls.py
from django.urls import path
from .views import MediaUploadView, MediaListView


urlpatterns = [
    path("upload/", MediaUploadView.as_view(), name="media-upload"),
    path("", MediaListView.as_view(), name="media-list"),
]
