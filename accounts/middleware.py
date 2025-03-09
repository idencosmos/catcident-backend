from django.shortcuts import redirect
from django.urls import reverse
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_email.models import EmailDevice


class OTPSetupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # admin 페이지에 접근하고 인증된 사용자인 경우에만 검사
        if request.user.is_authenticated and request.path.startswith("/admin/"):
            # 로그인/로그아웃 URL은 통과
            if any(url in request.path for url in ['/admin/login/', '/admin/logout/']):
                return self.get_response(request)
                
            has_totp = TOTPDevice.objects.filter(
                user=request.user, confirmed=True
            ).exists()
            has_email_otp = EmailDevice.objects.filter(
                user=request.user, confirmed=True
            ).exists()
            
            # OTP 장치가 없으면 설정 페이지로
            if not (has_totp or has_email_otp):
                return redirect(reverse("setup_otp"))
                
            # OTP 검증이 안 된 경우 검증 페이지로
            if not request.user.is_verified():
                print("User not verified, redirecting to verify_otp")
                return redirect(reverse("verify_otp"))
                
        return self.get_response(request)
