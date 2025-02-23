# config/urls.py


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from uploads.views import CKEditor5UploadView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/uploads/', include('uploads.urls')),  # uploads app의 API
    path("api/homepage/", include("homepage.urls")),  # homepage app의 API
    path('ckeditor5/image_upload/', CKEditor5UploadView.as_view(), name='ckeditor5-upload'),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
