# catcident-backend

```
# 개발환경 명령어
docker-compose -f docker-compose.dev.yml up --build -d

# 심볼릭 링크 생성
ln -sf docker-compose.dev.yml docker-compose.yml
```

```
# 프로덕션 환경 명령어
docker-compose -f docker-compose.prod.yml up --build -d
```

```bash
# 예시 (docker-compose.yml 파일에 정의된 서비스 이름이 'web'인 경우)
docker compose run api python manage.py collectstatic
docker compose run api python manage.py makemigrations
docker compose run api python manage.py migrate
docker compose run api python manage.py createsuperuser
```

```bash
# 기본 데이터 로드 명령어
docker compose run api python manage.py loaddata fixtures/initial_data.json
```
