# sp-server

## 시작 방법

- 도커를 이용하지 않을 경우

1. 의존성 설치

```
pip install -r requirements.txt
```

2. 서버 실행

```
python manage.py runserver 0.0.0.0:8000
```

- 도커를 이용할 경우

1. 이미지 빌드

```
docker build -t sp-server-image .
```

2. 컨테이너 실행

```
docker run -it --rm -p 8000:8000 sp-server-image
```