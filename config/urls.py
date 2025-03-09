from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import (
    CustomLoginView,
    setup_otp,
    setup_totp,
    setup_email_otp,
    OTPVerifyView,
)
from uploads.views import CKEditor5UploadView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("otp/setup/", setup_otp, name="setup_otp"),
    path("otp/setup-totp/", setup_totp, name="setup_totp"),
    path("otp/setup-email/", setup_email_otp, name="setup_email_otp"),
    path("otp/verify/", OTPVerifyView.as_view(), name="verify_otp"),
    path("api/uploads/", include("uploads.urls")),
    path("api/homepage/", include("homepage.urls")),
    path(
        "ckeditor5/image_upload/",
        CKEditor5UploadView.as_view(),
        name="ckeditor5-upload",
    ),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
