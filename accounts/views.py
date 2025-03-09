from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_email.models import EmailDevice
from django.shortcuts import redirect, render
from django.urls import reverse
from django_otp.forms import OTPTokenForm
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import qrcode
from io import BytesIO
import base64
import django_otp
from django_otp import match_token, devices_for_user
from django_otp.models import Device
from django.contrib import messages


# 로그인 뷰
class CustomLoginView(LoginView):
    template_name = "otp/login.html"
    authentication_form = AuthenticationForm

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user
        has_totp = TOTPDevice.objects.filter(user=user, confirmed=True).exists()
        has_email_otp = EmailDevice.objects.filter(user=user, confirmed=True).exists()
        
        if not (has_totp or has_email_otp):
            messages.info(self.request, "보안 강화를 위해 2단계 인증을 설정해주세요.")
            return redirect("setup_otp")
        
        if not user.is_verified():
            return redirect("verify_otp")
            
        return redirect("admin:index")


# OTP 설정 선택 뷰
@login_required
def setup_otp(request):
    if request.method == "POST":
        otp_type = request.POST.get("otp_type")
        if otp_type == "totp":
            return redirect("setup_totp")
        elif otp_type == "email":
            return redirect("setup_email_otp")
    return render(request, "otp/setup_otp.html")


# TOTP 설정 뷰
@login_required
def setup_totp(request):
    device, created = TOTPDevice.objects.get_or_create(
        user=request.user,
        name=f"{request.user.username}_totp",
        defaults={"confirmed": False},
    )
    
    if request.method == "POST":
        token = request.POST.get("token")
        if device.verify_token(token):
            device.confirmed = True
            device.save()
            messages.success(request, "TOTP 인증이 성공적으로 설정되었습니다.")
            return redirect("admin:index")
        return render(
            request,
            "otp/setup_totp.html",
            {"qr_code": qr_code_img, "error": "잘못된 인증 코드입니다. 다시 시도해주세요."},
        )

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(device.config_url)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    qr_code_img = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return render(request, "otp/setup_totp.html", {"qr_code": qr_code_img})


# 이메일 OTP 설정 뷰
@login_required
def setup_email_otp(request):
    device, created = EmailDevice.objects.get_or_create(
        user=request.user,
        name=f"{request.user.username}_email",
        defaults={"confirmed": False},
    )
    
    if request.method == "POST":
        token = request.POST.get("token")
        if device.verify_token(token):
            device.confirmed = True
            device.save()
            messages.success(request, "이메일 OTP 인증이 성공적으로 설정되었습니다.")
            return redirect("admin:index")
        return render(request, "otp/setup_email.html", {"error": "잘못된 인증 코드입니다. 다시 시도해주세요."})
        
    device.generate_challenge()
    return render(request, "otp/setup_email.html")


# OTP 검증 뷰
class OTPVerifyView(LoginRequiredMixin, FormView):
    template_name = "otp/verify_otp.html"
    form_class = OTPTokenForm
    success_url = "/admin/"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """
        사용자의 모든 OTP 장치를 직접 확인하고 인증하는 방식으로 수정
        """
        user = self.request.user
        token = form.cleaned_data.get('otp_token')
        
        # 사용자의 모든 장치 확인
        for device in devices_for_user(user):
            if device.verify_token(token):
                # 장치 인증 성공
                django_otp.login(self.request, device)
                self.request.session['otp_device_id'] = device.persistent_id
                messages.success(self.request, "2단계 인증이 완료되었습니다.")
                return redirect(self.success_url)
        
        # 여기까지 왔다면 모든 장치에서 인증 실패
        return self.render_to_response(
            self.get_context_data(form=form, error="잘못된 인증 코드입니다. 다시 시도해주세요.")
        )

    def form_invalid(self, form):
        # 특별히 otp_token 필드의 오류 처리
        if 'otp_token' in form.errors:
            return self.render_to_response(
                self.get_context_data(form=form, error="잘못된 인증 코드입니다. 다시 시도해주세요.")
            )
            
        return self.render_to_response(
            self.get_context_data(form=form, error="폼 검증에 실패했습니다. 다시 시도해주세요.")
        )
    
    def post(self, request, *args, **kwargs):
        """
        폼 제출 처리를 직접 처리하여 OTPTokenForm의 유효성 검사 방식 개선
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        # POST 데이터에서 직접 토큰 추출
        token = request.POST.get(form.add_prefix('otp_token'))
        if token:
            # 토큰이 6자리 숫자인지 검증
            if len(token) == 6 and token.isdigit():
                user = request.user
                # 모든 사용자 장치에서 토큰 검증
                for device in devices_for_user(user):
                    if device.verify_token(token):
                        django_otp.login(request, device)
                        request.session['otp_device_id'] = device.persistent_id
                        messages.success(request, "2단계 인증이 완료되었습니다.")
                        return redirect(self.success_url)
            
            # 토큰 유효성 검증 실패
            return self.render_to_response(
                self.get_context_data(form=form, error="잘못된 인증 코드입니다. 다시 시도해주세요.")
            )
        
        # 토큰이 없는 경우 폼 자체가 유효하지 않음
        return self.render_to_response(
            self.get_context_data(form=form, error="인증 코드가 필요합니다.")
        )