# CatCident Backend

다국어 지원 콘텐츠 관리 시스템(CMS) 및 REST API 서버

## 📌 프로젝트 개요

CatCident Backend는 [고양이의 만행] 사이트를 위한 Django 기반 콘텐츠 관리 시스템입니다. 다국어 지원(한국어/영어)을 통해 국내외 사용자에게 콘텐츠를 제공합니다.

## 🚀 주요 기능

- **완전한 다국어 지원**: `django-parler`를 활용한 모델 번역 기능
- **콘텐츠 관리 시스템**: 사이트 내용을 관리하기 위한 Django Admin 인터페이스
- **RESTful API**: 프론트엔드 애플리케이션에 데이터를 제공하는 API
- **미디어 파일 관리**: 클라우드 스토리지(Cloudflare R2) 통합
- **비동기 작업 처리**: Celery와 Redis를 활용한 백그라운드 작업
- **보안 인증 시스템**: 2단계 인증(OTP)을 통한 관리자 보안 강화
- **다양한 OTP 옵션**: TOTP(Google/Microsoft Authenticator) 및 이메일 OTP 지원

## 🏗️ 기술 스택

- **백엔드**: Django 5.1, Django REST Framework
- **데이터베이스**: PostgreSQL
- **캐싱 및 메시지 큐**: Redis
- **비동기 작업**: Celery
- **스토리지**: Cloudflare R2 (S3 호환)
- **컨테이너화**: Docker, Docker Compose
- **보안**: Django OTP

## 📋 주요 앱 구조

### 1. Homepage 앱
- 메인 CMS 기능 담당
- 글로벌 설정(네비게이션, 푸터 등)
- 홈페이지 섹션 및 슬라이드
- 콘텐츠 섹션(소개, 도서, 뉴스, 이벤트 등)

### 2. Uploads 앱
- 미디어 파일 관리
- R2 스토리지 연동
- 파일 사용 추적 및 미사용 파일 정리

### 3. Accounts 앱
- 사용자 인증 및 권한 관리
- 2단계 인증(OTP) 관리
  - TOTP(시간 기반 일회용 비밀번호) 인증
  - 이메일 기반 OTP 인증
  - 인증 시도 제한 및 차단 기능

## 💾 모델 구조

### Global Models
- `SiteTitle`: 사이트 제목
- `NavigationGroup`, `NavigationSubMenu`: 네비게이션 메뉴
- `FooterSection`, `FooterSubMenu`: 푸터 메뉴
- `FamilySite`: 연관 사이트 링크
- `Copyright`: 저작권 정보

### Home Models
- `HomeSection`: 홈페이지 섹션 관리(도서, 작가, 뉴스, 이벤트 등)
- `HeroSlide`: 메인 슬라이더

### About Models
- `Creator`: 작가/창작자 정보
- `BookCategory`, `Book`: 도서 카테고리 및 도서 정보
- `Character`: 캐릭터 정보
- `HistoryEvent`: 연혁 정보
- `LicensePage`: 라이선스 페이지

### Resources Models
- `ResourceCategory`, `Resource`: 리소스 자료

### News/Events Models
- `NewsCategory`, `News`: 뉴스 카테고리 및 뉴스
- `EventCategory`, `Event`: 이벤트 카테고리 및 이벤트

### Uploads Model
- `Media`: 미디어 파일 관리 및 사용 추적

## 🛠️ 개발 환경 설정

### 필수 조건
- Docker 및 Docker Compose
- Python 3.11 이상(로컬 개발 시)

### 개발 환경 실행

1. 리포지토리 클론
```bash
git clone <repository-url>
cd catcident-backend
```

2. 개발용 docker-compose 심볼릭 링크 생성
```bash
ln -sf docker-compose.dev.yml docker-compose.yml
```

3. 환경 변수 설정 (.env 파일 생성)
```
SECRET_KEY=your-secret-key
DEBUG=True
POSTGRES_DB=catcident
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
R2_BUCKET_NAME=your-bucket-name
R2_REGION=auto
R2_ENDPOINT_URL=https://xxx.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=your-access-key
R2_SECRET_ACCESS_KEY=your-secret-key
MEDIA_PUBLIC_DOMAIN=https://example.com
STATIC_URL=/static/
MEDIA_URL=/media/
STATICFILES_STORAGE=uploads.storages.StaticStorage
DEFAULT_FILE_STORAGE=uploads.storages.MediaStorage
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost,http://127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# OTP 설정
OTP_TOTP_ISSUER=Catcident API
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=your-smtp-host
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-email-password
OTP_EMAIL_SUBJECT=Your OTP Token
OTP_EMAIL_BODY_TEMPLATE=Your one-time password is: {{ token }}
```

4. 도커 컨테이너 실행
```bash
docker-compose up --build -d
```

### 데이터베이스 초기화

1. 모델 변경사항 마이그레이션 파일 생성
```bash
docker compose run api python manage.py makemigrations
```

2. 마이그레이션 적용
```bash
docker compose run api python manage.py migrate
```

3. 관리자 계정 생성
```bash
docker compose run api python manage.py createsuperuser
```

4. 초기 데이터 로드
```bash
docker compose run api python manage.py loaddata fixtures/initial_data.json
```

> **참고**: 모델을 변경한 후에는 항상 `makemigrations`를 실행하여 변경사항을 마이그레이션 파일로 생성한 후 `migrate`로 적용해야 합니다.

## 🚢 프로덕션 배포

1. 프로덕션용 docker-compose 설정 사용
```bash
ln -sf docker-compose.prod.yml docker-compose.yml
```

2. 프로덕션 환경 변수 설정 (.env 파일)
```
DEBUG=False
...기타 프로덕션 설정...
```

3. 배포 실행
```bash
docker-compose up --build -d
```

4. 정적 파일 수집
```bash
docker compose run api python manage.py collectstatic --no-input
```

## 🔒 보안 기능

### 2단계 인증 (OTP)

관리자 패널에 대한 보안 강화를 위해 2단계 인증을 구현했습니다:

1. **인증 방식 선택**
   - TOTP: Google/Microsoft Authenticator 앱 사용
   - 이메일: 등록된 이메일로 OTP 코드 전송

2. **보안 기능**
   - 로그인 후 OTP 설정 강제
   - 5회 인증 실패 시 10분간 차단
   - 이메일 OTP 재전송 30초 제한
   - IP 및 User-Agent 검증을 통한 세션 보안

3. **OTP 설정 방법**
   - 관리자 로그인 후 자동으로 OTP 설정 페이지로 이동
   - TOTP: QR 코드 스캔 후 인증 코드 입력
   - 이메일: 전송된 인증 코드 입력

## 📝 API 문서

주요 API 엔드포인트:

- `/api/homepage/global/` - 글로벌 설정(사이트 제목, 네비게이션, 푸터 등)
- `/api/homepage/home/` - 홈페이지 섹션 및 슬라이드
- `/api/homepage/about/` - 작가, 도서, 캐릭터, 연혁 등
- `/api/homepage/resources/` - 리소스 자료
- `/api/homepage/news/` - 뉴스 콘텐츠
- `/api/homepage/events/` - 이벤트 정보
- `/api/uploads/` - 미디어 파일 업로드 API

## 🔧 유지보수

### 미디어 파일 관리
미사용 파일은 자동으로 정리됩니다(Celery 작업). 관리자 패널의 "Media" 섹션에서 수동으로 관리할 수도 있습니다.

### 백업
데이터베이스와 미디어 파일의 정기적인 백업을 권장합니다.

## 📄 라이선스

이 프로젝트는 MIT 라이선스로 배포됩니다. 자세한 내용은 [LICENSE](./LICENSE) 파일을 참조하세요.
