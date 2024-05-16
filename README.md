# MementoAI_Backend_Assginment

## 개요

원본 URL 받아서 그와 매핑된 단축 Key반환 해주고, 해당 단축 Key로 조회 시, 원본 URL로 리디렉션 해주는 서비스

## 프로젝트 구조

```
MementoAI_Backend_Assginment
├─ .gitignore
├─ Pipfile
├─ README.md
├─ app
│  ├─ requirements.txt : Dependencies
│  ├─ alembic : Alembic
│  ├─ alembic.ini
│  ├─ api : EndPoint
│  │  └─ v1
│  │     ├─ router.py
│  │     └─ url_mapping.py
│  ├─ core : Env Setting
│  ├─ crud : 비즈니스 로직
│  │  ├─ selectors : Read
│  │  ├─ services : Create / Update / Delete
│  ├─ db : Sqlalchmey 설정 및 Session
│  ├─ exception : 사용자 정의 Exception
│  ├─ main.py
│  ├─ models : Sqlalchemy Models
│  ├─ schemas : Pydantic Schemas
│  ├─ tests : Pytest
│  │  ├─ conftest.py : Fixtures
│  │  ├─ fixtures
│     └─ v1 : Endpoint test code
├─ docker-compose.yml
└─ dockerfile
```

## 기능 설명

### 단축 Key 생성

원본 URL 받아서 UrlMapping 객체 생성 및 단축 Key 반환

- EndPoint : POST "v1/shorten"
- Parameters : 
    - url_in (UrlMappingCreate)
        - origin_url (required) : 원본 URL
        - expire_date : 만료기한
- Returns:
    - UrlMappingResponse
        - origin_url : 원본 URL
        - expire_date : 만료기한
        - shorten_key : 단축 Key
        - view_count : 조회 수

### 원본 URL 리디렉션

단축 Key를 받아서 해당 Key 매핑 된 UrlMapping 객체 반환 및 조회수 증가

- EndPoint : GET "v1/{shorten_key}"
- Parameters : 
    - shorten_key : 단축 Key
- Raises:
    - 단축 Key에 해당하는 URL이 없을 경우 404
    - 유효기간이 만료된 경우 404
- Returns:
    - UrlMappingResponse
        - origin_url : 원본 URL
        - expire_date : 만료기한
        - shorten_key : 단축 Key
        - view_count : 조회 수


### 조회 수 확인

단축 Key 받아서 해당 Key의 조회 수 확인

- EndPoint : GET "v1/stats/{shorten_key}"
- Parameters : 
    - shorten_key : 단축 Key
- Raises:
    - 단축 Key에 해당하는 URL이 없을 경우 404
- Returns:
    - UrlMappingResponse
        - origin_url : 원본 URL
        - expire_date : 만료기한
        - shorten_key : 단축 Key
        - view_count : 조회 수


### 전체 UrlMapping 조회

전체 UrlMapping 목록 조회

- EndPoint : GET "v1/shortens"
- Returns:
    - List[UrlMappingResponse]
        - origin_url : 원본 URL
        - expire_date : 만료기한
        - shorten_key : 단축 Key
        - view_count : 조회 수

### 만료 기한 수정

expire_date 수정

- EndPoint : GET "v1/shorten/{shorten_key}"
- Parameters : 
    - update_in (UrlMappingUpdate)
        - expire_date : 만료기한
- Raises:
    - 단축 Key에 해당하는 URL이 없을 경우 404
- Returns:
    - UrlMappingResponse
        - origin_url : 원본 URL
        - expire_date : 만료기한
        - shorten_key : 단축 Key
        - view_count : 조회 수

## Start

1. Clone the git repo

    ```
    git clone https://github.com/Hyun-Jun-Lee/MementoAI_Backend_Assginment.git
    
    cd MementoAI_Backend_Assginment.git
    ```

2. `.env` 생성 (env.sample 참고)

3. docker container 실행

    ```
    docker compose up
    ```

4. Alembic Migrations

    ```
    docker compose run --rm backends alembic upgrade head
    ```

## Test

```
docker compose run --rm pytest
```

## Swagger

"http://0.0.0.0:8000/docs"

![image](https://github.com/Hyun-Jun-Lee/MementoAI_Backend_Assginment/assets/76996686/a4a561f4-72af-4adb-9de9-4cac34b8f323)
