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