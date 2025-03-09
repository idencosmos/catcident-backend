from django.contrib.auth.models import AbstractUser
from django.db import models
from django_otp import user_has_device


class CustomUser(AbstractUser):
    is_approved = models.BooleanField(default=False, help_text="관리자 승인 여부")

    def has_perm(self, perm, obj=None):
        if not self.is_approved and not self.is_superuser:
            return False
        return super().has_perm(perm, obj)

    def is_verified(self):
        """
        장고 OTP 인증 여부를 확인하는 메서드
        """
        return user_has_device(self) and self.otp_device is not None
