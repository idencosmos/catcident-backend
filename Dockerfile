# Builder 단계: 의존성 설치 전용
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Poetry 설치
RUN pip install --upgrade pip && \
    pip install poetry

# 의존성 파일 복사 및 설치
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && \
    poetry install --no-root

# 최종 이미지
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# 시스템 의존성 및 curl 설치 (헬스체크용)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 비루트 사용자 생성
RUN groupadd -r django && \
    useradd -r -g django django && \
    chown -R django:django /app

# Builder 단계에서 설치된 Python 의존성 복사
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 프로젝트 파일 복사
COPY --chown=django:django . .

# 환경 변수로 Django 설정 모듈 지정
ARG DJANGO_SETTINGS_MODULE=config.settings.production
ENV DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}

# 권한 설정
RUN chmod -R 755 /app

# 비루트 사용자로 전환
USER django

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]