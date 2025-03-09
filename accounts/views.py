# Django imports
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

# Third party imports
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_email.models import EmailDevice
from django_otp.forms import OTPTokenForm
from django_otp import devices_for_user, login as otp_login
from django_otp.models import Device

# Python standard library
from datetime import timedelta, datetime
import qrcode
from io import BytesIO
import base64


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
    # 사용자당 TOTP 디바이스 1개만 허용
    existing_totp = TOTPDevice.objects.filter(user=request.user, confirmed=True).count()
    if existing_totp >= 1:
        messages.error(request, "이미 등록된 TOTP 디바이스가 있습니다.")
        return redirect("admin:index")

    # device 객체 가져오기 또는 생성
    device, created = TOTPDevice.objects.get_or_create(
        user=request.user,
        confirmed=False,
        defaults={"name": f"{request.user.username}_totp"},
    )

    # QR 코드 생성 함수
    def generate_qr_code(device):
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(device.config_url)
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    # QR 코드 생성
    qr_code_img = generate_qr_code(device)

    if request.method == "POST":
        token = request.POST.get("token")
        if token and device.verify_token(token):
            device.confirmed = True
            device.save()
            messages.success(request, "TOTP 인증이 성공적으로 설정되었습니다.")
            return redirect("admin:index")

        # 토큰 검증 실패 시 같은 QR 코드로 다시 시도
        return render(
            request,
            "otp/setup_totp.html",
            {
                "qr_code": qr_code_img,
                "error": "잘못된 인증 코드입니다. 다시 시도해주세요.",
            },
        )

    return render(request, "otp/setup_totp.html", {"qr_code": qr_code_img})


# 이메일 OTP 설정 뷰
@login_required
def setup_email_otp(request):
    # 사용자당 이메일 디바이스 1개만 허용
    existing_email = EmailDevice.objects.filter(
        user=request.user, confirmed=True
    ).count()
    if existing_email >= 1:
        messages.error(request, "이미 등록된 이메일 OTP 디바이스가 있습니다.")
        return redirect("admin:index")

    # device 객체 가져오기 또는 생성
    device, created = EmailDevice.objects.get_or_create(
        user=request.user,
        confirmed=False,
        defaults={"name": f"{request.user.username}_email"},
    )

    # 재발송 요청 처리
    if request.method == "POST" and request.POST.get("action") == "resend":
        last_sent = request.session.get("last_email_otp_sent")
        current_time = timezone.now().timestamp()

        if last_sent and current_time - float(last_sent) < 30:
            remaining = int(30 - (current_time - float(last_sent)))
            messages.error(request, f"{remaining}초 후에 재발송할 수 있습니다.")
        else:
            device.generate_challenge()
            request.session["last_email_otp_sent"] = current_time
            messages.success(request, "인증 코드를 재발송했습니다.")
        return render(request, "otp/setup_email.html")

    if request.method == "POST" and request.POST.get("token"):
        token = request.POST.get("token")
        if device.verify_token(token):
            device.confirmed = True
            device.save()
            messages.success(request, "이메일 OTP 인증이 성공적으로 설정되었습니다.")
            return redirect("admin:index")
        else:
            messages.error(request, "잘못된 인증 코드입니다.")
            return render(request, "otp/setup_email.html")

    # 초기 이메일 발송 (GET 요청 또는 새로 생성된 경우)
    if created or request.method == "GET":
        device.generate_challenge()
        current_time = timezone.now().timestamp()
        request.session["last_email_otp_sent"] = current_time
        # 중복 메시지 제거, 하나만 표시
        messages.info(request, "등록된 이메일로 인증 코드가 발송되었습니다.")

    return render(request, "otp/setup_email.html")


class OTPVerifyView(LoginRequiredMixin, FormView):
    template_name = "otp/verify_otp.html"
    form_class = OTPTokenForm
    success_url = reverse_lazy("admin:index")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 현재 사용자의 이메일 OTP 디바이스 확인
        context["is_email_device"] = EmailDevice.objects.filter(
            user=self.request.user, confirmed=True
        ).exists()
        return context

    def post(self, request, *args, **kwargs):
        # 재발송 요청 처리
        if request.POST.get("action") == "resend":
            device = EmailDevice.objects.filter(
                user=request.user, confirmed=True
            ).first()
            if device:
                last_sent = request.session.get("last_email_otp_sent")
                current_time = timezone.now().timestamp()

                if last_sent and current_time - float(last_sent) < 30:
                    remaining = int(30 - (current_time - float(last_sent)))
                    messages.error(request, f"{remaining}초 후에 재발송할 수 있습니다.")
                else:
                    device.generate_challenge()
                    request.session["last_email_otp_sent"] = current_time
                    messages.success(request, "인증 코드를 재발송했습니다.")
            return self.get(request, *args, **kwargs)

        # 기존의 OTP 검증 로직
        fail_count = request.session.get("otp_fail_count", 0)
        ban_start_str = request.session.get("otp_ban_start")
        max_attempts = 5
        ban_duration = 10  # minutes

        if ban_start_str:
            ban_start = datetime.fromisoformat(ban_start_str)
            time_passed = timezone.now() - ban_start
            if time_passed < timedelta(minutes=ban_duration):
                remaining_time = int(
                    (timedelta(minutes=ban_duration) - time_passed).total_seconds() / 60
                )
                return render(
                    request,
                    self.template_name,
                    {
                        "form": self.get_form(self.form_class),
                        "error": f"인증 실패 횟수 초과로 {remaining_time}분 후에 다시 시도해주세요.",
                    },
                )
            else:
                request.session["otp_ban_start"] = None
                request.session["otp_fail_count"] = 0
                fail_count = 0

        token = request.POST.get("otp_token")
        if token and len(token) == 6 and token.isdigit():
            user = request.user
            for device in devices_for_user(user):
                if device.verify_token(token):
                    request.session["otp_fail_count"] = 0
                    otp_login(request, device)
                    request.session["otp_device_id"] = device.persistent_id
                    messages.success(request, "2단계 인증이 완료되었습니다.")
                    return redirect(self.success_url)

            fail_count += 1
            request.session["otp_fail_count"] = fail_count
            remaining_attempts = max_attempts - fail_count

            if fail_count >= max_attempts:
                request.session["otp_ban_start"] = timezone.now().isoformat()
                error_message = f"인증 실패 횟수({max_attempts}회)를 초과했습니다. {ban_duration}분 후에 다시 시도해주세요."
            else:
                error_message = (
                    f"잘못된 인증 코드입니다. 남은 시도 횟수: {remaining_attempts}회"
                )

            return render(
                request,
                self.template_name,
                {
                    "form": self.get_form(self.form_class),
                    "error": error_message,
                },
            )
        else:
            return render(
                request,
                self.template_name,
                {
                    "form": self.get_form(self.form_class),
                    "error": "6자리 숫자 코드를 입력해주세요.",
                },
            )


# 세션 하이재킹 방지를 위한 IP/User-Agent 확인 예시


def check_session_security(request):
    current_ip = request.META.get("REMOTE_ADDR")
    current_ua = request.META.get("HTTP_USER_AGENT", "")
    initial_ip = request.session.get("initial_ip")
    initial_ua = request.session.get("initial_ua")

    if not initial_ip or not initial_ua:
        # 최초 로그인 시 저장
        request.session["initial_ip"] = current_ip
        request.session["initial_ua"] = current_ua
    else:
        # 로그인 후 다른 IP/UA로 바뀌면 로그아웃 처리 등
        if current_ip != initial_ip or current_ua != initial_ua:
            messages.error(request, "세션 보안이 의심됩니다. 다시 로그인하세요.")
            return redirect("logout")


def logout_view(request):
    # 로그아웃 시 OTP 관련 세션 데이터 초기화
    if "otp_fail_count" in request.session:
        del request.session["otp_fail_count"]
    if "otp_ban_start" in request.session:
        del request.session["otp_ban_start"]
    if "initial_ip" in request.session:
        del request.session["initial_ip"]
    if "initial_ua" in request.session:
        del request.session["initial_ua"]
    return redirect("login")
