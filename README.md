# ALWIDA_server
(주)Finder 외주용역

----

## git clone 후 실행해야할 리스트

- `docker-compose.yml`에서 사용할 변수 파일인 `.env` 파일 생성
- `ALWIDA_admin` 폴더와 `ALWIDA_app_data` 폴더에 MariaDB에 연결할 내용을 기술하는 config.ini 파일 생성

----

## 서버 실행 방법

```bash
docker-compose up
```

----

## 파일 설명

- `ALWIDA_admin` : 관리자페이지에 대한 소스코드
- `ALWIDA_app_data` : app과 통신할때 필요한 웹 서버
- `MariaDB` : DB의 데이터가 `data` 폴더안 들어있음.
